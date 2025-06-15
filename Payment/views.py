import stripe
import logging
from decouple import config
from django.shortcuts import redirect 


from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import  views 
from rest_framework import  status 
from rest_framework import  permissions
from rest_framework import  throttling 


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404 


from Cart.models import OrderModel 
from Cart.models import OrderItemModel 


from core.paymentprocessor import PaymentProcessor 


from .models import PaymentModel
from .models import PayPalPaymentModel  
from .serializers import OrderPaymentProcessorSerializer 
from core.core_permissions import CartItemIsOwnerStaffOrSuperUser 


stripe.api_key = config("STRIPE_TEST_SECRET_KEY")


logger = logging.getLogger(__name__)

User = get_user_model()


class PaymentViewSet(viewsets.ModelViewSet):
    """ 
    A viewset for handling payment-related operations.
    This viewset allows authenticated users to create a Stripe checkout session
    for their unpaid orders, confirming the order before proceeding to payment.
    - Uses the `OrderPaymentProcessorSerializer` to validate input data.
    - Ensures the user is authenticated and has an unpaid order.
    - Creates a Stripe checkout session with the order details.
    - Returns the checkout URL for the user to complete the payment.
    - Handles errors gracefully, returning appropriate HTTP responses.
    """ 
    queryset = OrderModel.objects.all()
    serializer_class = OrderPaymentProcessorSerializer
    permission_classes = [permissions.IsAuthenticated, CartItemIsOwnerStaffOrSuperUser]
    http_method_names = ['get', 'post']
    throttle_classes = [throttling.UserRateThrottle]

    @action(detail=False, methods=['post'], url_path='create-checkout-session')
    def create_checkout_session(self, request):
        """
        Create a Stripe checkout session for the current user's unpaid order.
        - Validates the request data using the serializer.
        - Ensures the user is authenticated and has confirmed the order.
        - Retrieves the user's unpaid order and its items.
        - Creates a Stripe checkout session and returns the checkout URL.
        - Handles and logs Stripe and server errors, returning appropriate HTTP responses.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # 400 Bad Request: The request data is invalid or missing required fields.
            return Response({
                "error": "Invalid input.",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        confirm = serializer.validated_data.get('confirm')
        if not confirm:
            # 400 Bad Request: The client did not confirm the order as required.
            return Response({
                "error": "Order confirmation required.",
                "message": "Please confirm the order before proceeding to payment."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            if not user.is_authenticated:
                # 401 Unauthorized: The user is not authenticated.
                return Response({
                    "error": "Authentication required.",
                    "message": "You must be logged in to create a checkout session."
                }, status=status.HTTP_401_UNAUTHORIZED)

            order = OrderModel.objects.filter(author=user, payment_status="unpaid").first()
            if not order:
                # 404 Not Found: No unpaid order found for the user.
                return Response({
                    "error": "No unpaid order found.",
                    "message": "You do not have any incomplete or unpaid orders to process."
                }, status=status.HTTP_404_NOT_FOUND)

            incomplate_order_items = OrderItemModel.objects.filter(order_id=order)
            order_id = order.id

            # frontend_url = f"{frontend_url}api/v1/stripe/success/?session_id={{CHECKOUT_SESSION_ID}}" 
            success_url = f"{request.scheme}://{request.get_host()}/api/v1/stripe/success/?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = f"{request.scheme}://{request.get_host()}/api/v1/stripe/cancel/"

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order #{order_id}',
                        },
                        'unit_amount': int(order.total_amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "order_id": str(order.id),
                    "user_id": str(user.id),
                }
            )

            # 200 OK: Stripe checkout session created successfully.
            return Response({
                "message": "Stripe checkout session created successfully.",
                "checkout_url": session.url
            }, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            # 502 Bad Gateway: Error communicating with Stripe API.
            logger.error("Stripe error: %s", str(e), exc_info=True)
            return Response({
                "error": "Payment gateway error.",
                "message": "There was a problem communicating with the payment provider. Please try again later."
            }, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            # 500 Internal Server Error: Unexpected server error.
            logger.error("Unexpected error: %s", str(e), exc_info=True)
            return Response({
                "error": "Internal server error.",
                "message": "An unexpected error occurred. Please contact support if the problem persists."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class StripeCancelApiView(views.APIView):
    """
    API view to handle Stripe payment cancellation.
    Returns a message indicating the payment was cancelled.
    """
    def get(self, request):
        # 200 OK: Payment was cancelled by the user
        return Response({"message": "Payment was cancelled."}, status=status.HTTP_200_OK)
    

    

logger = logging.getLogger(__name__)

class StripeSuccessApiView(APIView):
    """
    API view to handle successful Stripe payments.
    - Retrieves the Stripe session and extracts payment data.
    - Creates a PaymentModel record for the transaction.
    - Updates the order status to reflect successful payment and fulfillment.
    - Returns the payment data or error messages as appropriate.
    """
    permission_classes = []

    def get(self, request):
        # Retrieve the session_id from the query parameters
        session_id = request.query_params.get("session_id")
        if not session_id:
            # 400 Bad Request: session_id is required
            return Response({"error": "Missing session_id"}, status=400)
        try:
            # Retrieve the Stripe session using the session_id
            session = stripe.checkout.Session.retrieve(session_id)

            session_data = session if isinstance(session, dict) else session.to_dict()
            successfull_payer_data = PaymentProcessor(session_data).get_payment_data()

            # Get the order and user objects from the payment data
            order = get_object_or_404(OrderModel, id=successfull_payer_data.get("order_id"))
            user = get_object_or_404(User, id=successfull_payer_data.get("user_id"))

            # Create a PaymentModel record for the successful payment
            PaymentModel.objects.create(
                order=order,
                user=user,
                amount_paid=successfull_payer_data.get("amount_paid"),
                currency=successfull_payer_data.get("currency"),
                stripe_checkout_id=successfull_payer_data.get("stripe_checkout_id"),
                stripe_payment_intent=successfull_payer_data.get("stripe_payment_intent"),
                stripe_payment_status=successfull_payer_data.get("stripe_payment_status"),
                stripe_payment_method=successfull_payer_data.get("payment_method"),
                receipt_url=session_data.get("receipt_url"),
                name_of_payer=successfull_payer_data.get("customer_name"),
                email_of_payer=successfull_payer_data.get("customer_email"),
            )

            # Update the order status to reflect payment and fulfillment
            order.payment_status = "paid"
            order.is_confirmed = True
            order.ord_status = "completed"
            order.shipping_status = "shipped"
            order.save()

            # 200 OK: Payment processed successfully
            return redirect(f"http://localhost:5173/orders")
            # return Response(successfull_payer_data, status=status.HTTP_200_OK)

        except OrderModel.DoesNotExist:
            # 404 Not Found: Order not found
            logger.error("Order with ID %s not found.", successfull_payer_data.get("order_id"))
            return Response({"error": "Order not found."}, status=404)

        except Exception as e:
            # 500 Internal Server Error: Stripe session retrieval or processing error
            logger.error("Stripe session retrieve error: %s", str(e))
            return Response({"error": str(e)}, status=500)

        except stripe.error.StripeError as e:
            # 500 Internal Server Error: Stripe API error
            logger.error("Stripe error: %s", str(e))
            return Response({"error": "Stripe error occurred."}, status=500)
        


from .paypal import paypalrestsdk 


class PayPalPayment(viewsets.ModelViewSet):
    """ 
    A viewset for handling payment-related operations.
    This viewset allows authenticated users to create a Stripe checkout session
    for their unpaid orders, confirming the order before proceeding to payment.
    - Uses the `OrderPaymentProcessorSerializer` to validate input data.
    - Ensures the user is authenticated and has an unpaid order.
    - Creates a Stripe checkout session with the order details.
    - Returns the checkout URL for the user to complete the payment.
    - Handles errors gracefully, returning appropriate HTTP responses.
    """ 
    queryset = OrderModel.objects.all()
    serializer_class = OrderPaymentProcessorSerializer
    permission_classes = [permissions.IsAuthenticated, CartItemIsOwnerStaffOrSuperUser]
    http_method_names = ['get', 'post']
    throttle_classes = [throttling.UserRateThrottle]

    @action(detail=False, methods=['post'], url_path='create-checkout-session')
    def create_checkout_session(self, request):
        """
        Create a Stripe checkout session for the current user's unpaid order.
        - Validates the request data using the serializer.
        - Ensures the user is authenticated and has confirmed the order.
        - Retrieves the user's unpaid order and its items.
        - Creates a Stripe checkout session and returns the checkout URL.
        - Handles and logs Stripe and server errors, returning appropriate HTTP responses.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # 400 Bad Request: The request data is invalid or missing required fields.
            return Response({
                "error": "Invalid input.",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        confirm = serializer.validated_data.get('confirm')
        if not confirm:
            # 400 Bad Request: The client did not confirm the order as required.
            return Response({
                "error": "Order confirmation required.",
                "message": "Please confirm the order before proceeding to payment."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            if not user.is_authenticated:
                # 401 Unauthorized: The user is not authenticated.
                return Response({
                    "error": "Authentication required.",
                    "message": "You must be logged in to create a checkout session."
                }, status=status.HTTP_401_UNAUTHORIZED)

            order = OrderModel.objects.filter(author=user, payment_status="unpaid").first()
            if not order:
                # 404 Not Found: No unpaid order found for the user.
                return Response({
                    "error": "No unpaid order found.",
                    "message": "You do not have any incomplete or unpaid orders to process."
                }, status=status.HTTP_404_NOT_FOUND)

            incomplate_order_items = OrderItemModel.objects.filter(order_id=order)
            order_id = order.id

            # frontend_url = f"{frontend_url}api/v1/stripe/success/?session_id={{CHECKOUT_SESSION_ID}}" 
            success_url = f"{request.scheme}://{request.get_host()}/api/v1/paypal/success/"
            cancel_url = f"{request.scheme}://{request.get_host()}/api/v1/paypal/cancel/"

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": success_url,
                    "cancel_url": cancel_url
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": f"Order #{order_id}",
                            "sku": f"order_{order_id}",
                            "price": str(order.total_amount),
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(order.total_amount),
                        "currency": "USD"
                    },
                    "description": f"Order #{order_id} payment"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        return Response({
                            "message": "PayPal payment created successfully.",
                            "checkout_url": approval_url
                        }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Failed to create PayPal payment.",
                    "details": payment.error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("PayPal payment creation error: %s", str(e), exc_info=True)
            return Response({
                "error": "Internal server error.",
                "message": "An unexpected error occurred while creating PayPal payment."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






import logging

class PayPalSuccessViewSet(APIView):
    """ """

    permission_classes = [permissions.AllowAny] 

    def get(self, request): 
        payment_id = request.query_params.get("paymentId")
        payer_id = request.query_params.get("PayerID")
        token = request.query_params.get("token") 


        if not payment_id or not payer_id:
            return Response({"error": "Missing paymentId or PayerID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = paypalrestsdk.Payment.find(payment_id)

            if payment.execute({"payer_id": payer_id}):
                transaction = payment.transactions[0]
                sku = transaction.item_list.items[0].sku
                order_id = sku.split("_")[-1]

                order = get_object_or_404(OrderModel, id=order_id)
                user_id = order.author.id if order.author else None

                PayPalPaymentModel.objects.create(
                    order=order,
                    user_id=user_id,
                    name_of_payer=f"{payment.payer.payer_info.first_name} {payment.payer.payer_info.last_name}",
                    email_of_payer=payment.payer.payer_info.email,
                    amount_paid=float(transaction.amount.total),
                    currency=transaction.amount.currency,
                    paypal_payment_id=payment.id,
                    paypal_payer_id=payer_id,
                    paypal_token=token,
                    paypal_payment_status=payment.state,
                )

                order.payment_status = "paid"
                order.is_confirmed = True
                order.ord_status = "completed"
                order.shipping_status = "shipped"
                order.save()

                return redirect("http://localhost:5173/orders")  # Replace with settings.FRONTEND_URL in prod
            else:
                logger.error(f"Payment execution failed for ID: {payment_id}")
                return Response({"error": "Payment execution failed."}, status=status.HTTP_400_BAD_REQUEST)
        except paypalrestsdk.ResourceNotFound as e:
            logger.error(f"PayPal payment not found: {str(e)}")
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND) 

            
              
class PayPalCancelView(views.APIView):
    """
    API view to handle PayPal payment cancellation.
    Returns a message indicating the payment was cancelled.
    """
    def get(self, request):
        # 200 OK: Payment was cancelled by the user
        return Response({"message": "Payment was cancelled."}, status=status.HTTP_200_OK)  
    

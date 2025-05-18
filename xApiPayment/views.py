
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import viewsets, views, status, permissions
from django.conf import settings
from django.contrib.auth import get_user_model
from decouple import config
from .models import PaymentModel
from .serializers import PaymentSerializer
from xApiCart.models import OrderModel

import stripe
import logging

# Stripe API Key
stripe.api_key = config("STRIPE_TEST_SECRET_KEY")

# User model
User = get_user_model()

logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['post'], url_path='create-checkout-session')
    def create_checkout_session(self, request):
        try:
            data = request.data
            order_id = data.get('order_id')

            if not order_id:
                return Response({'error': 'order_id is required.'}, status=400)

            try:
                order = OrderModel.objects.get(id=order_id)
            except OrderModel.DoesNotExist:
                return Response({'error': 'Order not found.'}, status=404)

            user = request.user if request.user.is_authenticated else order.user

            success_url=f"{request.scheme}://{request.get_host()}/api/v1/stripe/success/?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url=f"{request.scheme}://{request.get_host()}/api/v1/stripe/cancel/"

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

            return Response({"checkout_url": session.url}, status=200)

        except stripe.error.StripeError as e:
            logger.error("Stripe error: %s", str(e), exc_info=True)
            return Response({"error": "Stripe error occurred."}, status=500)

        except Exception as e:
            logger.error("Unexpected error: %s", str(e), exc_info=True)
            return Response({"error": "Unexpected server error."}, status=500)


class StripeSuccessApiView(views.APIView):

    def get(self, request):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response({"error": "Missing session_id"}, status=400)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            customer = stripe.Customer.retrieve(session.customer)

            # Optionally save payment to DB
            PaymentModel.objects.create(
                order_id=session.metadata.get("order_id"),
                user_id=session.metadata.get("user_id"),
                amount=session.amount_total / 100,
                currency=session.currency.upper(),
                payment_status=session.payment_status,
                stripe_session_id=session.id
            )

            return Response({
                "success": True,
                "message": "Payment retrieved successfully",
                "data": {
                    "email": customer.email,
                    "amount_total": session.amount_total / 100,
                    "currency": session.currency.upper(),
                    "payment_status": session.payment_status,
                    "session_id": session.id
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            raise ParseError(f"An error occurred: {str(e)}")


class StripeCancelApiView(views.APIView):
    def get(self, request):
        return Response({"message": "Payment was cancelled."}, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
import logging

logger = logging.getLogger(__name__)

class StripeSuccessApiView(APIView):
    permission_classes = []

    def get(self, request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"error": "Missing session_id"}, status=400)

        try:
            session = stripe.checkout.Session.retrieve(session_id)

            # Convert Stripe object to plain dictionary
            session_data = session.to_dict()

            return Response(session_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Stripe session retrieve error: %s", str(e))
            return Response({"error": str(e)}, status=500)




class StripeCancelApiView(views.APIView):
    def get(self, request):
        """
        Handle cancelled payment.
        """
        return Response({"message": "Payment was cancelled."}, status=status.HTTP_200_OK) 




# import stripe
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from .models import PaymentModel
# from xApiCart.models import OrderModel
# from django.contrib.auth import get_user_model

# User = get_user_model()

# stripe.api_key = settings.STRIPE_SECRET_KEY


# class StripeSuccessView(APIView):
#     """
#     View to handle Stripe success callback and store payment data
#     """

#     def get(self, request):
#         session_id = request.GET.get("session_id")
#         if not session_id:
#             return Response({"error": "Missing session_id"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             session = stripe.checkout.Session.retrieve(session_id)

#             # Extract metadata
#             order_id = session.get("metadata", {}).get("order_id")
#             user_id = session.get("metadata", {}).get("user_id")

#             # Get related objects
#             try:
#                 order = OrderModel.objects.get(id=order_id)
#                 user = User.objects.get(id=user_id)
#             except (OrderModel.DoesNotExist, User.DoesNotExist):
#                 return Response({"error": "Invalid user or order ID"}, status=status.HTTP_404_NOT_FOUND)

#             # Check if already saved to prevent duplication
#             if PaymentModel.objects.filter(stripe_checkout_id=session.get("id")).exists():
#                 return Response({"message": "Payment already recorded."}, status=status.HTTP_200_OK)

#             # Retrieve PaymentIntent to get receipt_url and payment_method
#             payment_intent_id = session.get("payment_intent")
#             payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

#             # Save payment to DB
#             PaymentModel.objects.create(
#                 order=order,
#                 user=user,
#                 amount_paid=session.get("amount_total"),
#                 currency=session.get("currency"),
#                 stripe_checkout_id=session.get("id"),
#                 stripe_payment_intent=payment_intent_id,
#                 stripe_payment_status=session.get("payment_status"),
#                 stripe_payment_method=payment_intent.get("payment_method"),
#                 receipt_url=payment_intent.get("charges", {}).get("data", [{}])[0].get("receipt_url")
#             )

#             return Response({
#                 "message": "Payment saved successfully.",
#                 "order_id": order_id,
#                 "user_id": user_id,
#                 "amount": session.get("amount_total"),
#                 "payment_status": session.get("payment_status"),
#                 "receipt_url": payment_intent.get("charges", {}).get("data", [{}])[0].get("receipt_url"),
#             }, status=status.HTTP_200_OK)

#         except stripe.error.InvalidRequestError as e:
#             return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.exceptions import ParseError
# from rest_framework import viewsets
# from rest_framework import  permissions
# from rest_framework import views 
# from rest_framework import status 
# from django.conf import settings 
# from django.contrib.auth import get_user_model
# from decouple import config

# import stripe
# import logging

# import stripe.error

# from .models import PaymentModel
# from .serializers import PaymentSerializer
# from xApiCart.models import OrderModel

# # Stripe API Key
# stripe.api_key = config("STRIPE_TEST_SECRET_KEY")

# # User model
# User = get_user_model()

# # Logger
# logger = logging.getLogger(__name__)


# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = PaymentModel.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.AllowAny]
#     http_method_names = ['get', 'post']

#     @action(detail=False, methods=['post'], url_path='create-checkout-session')
#     def create_checkout_session(self, request):


#         try:
#             data = request.data

#             order_id = data.get('order_id')
#             if not order_id:
#                 return Response({'error': 'order_id is required.'}, status=400)

#             try:
#                 order = OrderModel.objects.get(id=order_id)
#             except OrderModel.DoesNotExist:
#                 return Response({'error': 'Order not found.'}, status=404)

#             user = request.user if request.user.is_authenticated else order.user

#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'usd',
#                         'product_data': {
#                             'name': f'Order #{order_id}',
#                         },
#                         'unit_amount': int(order.total_amount * 100),
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 success_url = request.build_absolute_uri(f"/api/v1/stripe/success/?session_id={{CHECKOUT_SESSION_ID}}"),
#                 cancel_url=request.build_absolute_uri('/api/v1/stripe/cancel/'),
#                 metadata={
#                     "order_id": str(order.id),
#                     "user_id": str(user.id),
#                 }
#             )

#             return Response({"checkout_url": session.url}, status=200)

#         except stripe.error.StripeError as e:
#             logger.error("Stripe error: %s", str(e), exc_info=True)
#             return Response({"error": "Stripe error occurred."}, status=500)

#         except Exception as e:
#             logger.error("Unexpected error: %s", str(e), exc_info=True)
#             return Response({"error": "Unexpected server error."}, status=500)
        


    # @action(detail=False, methods=['get'], url_path="success")
    # def success(self, request):
    #     """
    #     Handle payment success callback with session_id
    #     """
    #     session_id = request.query_params.get("session_id")
    #     if not session_id:
    #         return Response({"error": "Missing session_id"}, status=400)

    #     try:
    #         session = stripe.checkout.Session.retrieve(session_id)
    #         payment_intent_id = session.payment_intent

    #         # Retrieve payment intent details
    #         payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

    #         # Get metadata
    #         order_id = session.metadata.get("order_id")
    #         user_id = session.metadata.get("user_id")

    #         try:
    #             order = OrderModel.objects.get(id=order_id)
    #             user = User.objects.get(id=user_id)
    #         except (OrderModel.DoesNotExist, User.DoesNotExist):
    #             return Response({"error": "Order or User not found"}, status=404)

    #         # Save payment info
    #         payment, created = PaymentModel.objects.get_or_create(
    #             stripe_checkout_id=session.id,
    #             defaults={
    #                 "order": order,
    #                 "user": user,
    #                 "amount_paid": payment_intent.amount_received / 100,
    #                 "currency": payment_intent.currency,
    #                 "stripe_payment_intent": payment_intent.id,
    #                 "stripe_payment_status": payment_intent.status,
    #                 "stripe_payment_method": payment_intent.payment_method,
    #                 "receipt_url": payment_intent.charges.data[0].receipt_url if payment_intent.charges.data else None,
    #             }
    #         )

    #         return Response({
    #             "message": "Payment successful!",
    #             "payment_id": payment.id,
    #             "receipt_url": payment.receipt_url,
    #             "status": payment.stripe_payment_status,
    #         })

    #     except stripe.error.StripeError as e:
    #         logger.error("Stripe error in success view: %s", str(e), exc_info=True)
    #         return Response({"error": "Stripe error occurred."}, status=500)

    #     except Exception as e:
    #         logger.error("Unexpected error in success view: %s", str(e), exc_info=True)
    #         return Response({"error": "Unexpected server error."}, status=500)



    # @action(detail=False, methods=['get'], url_path="cancel")
    # def cancel(self, request):
    #     """
    #     Handle cancelled payment.
    #     """
    #     return Response({"message": "Payment was cancelled."}, status=200)




# class StripeSuccessApiView(views.APIView):

#     def get(self, request):
#         session_id  = request.query_params.get("session_id") 

#         if not session_id:
#             return Response({"error": "Missing session_id"}, status=400) 
        
#         try:
#             session  = stripe.checkout.Session.retrieve(session_id) 
#             customer = stripe.Customer.retrieve(session.customer)

#             return Response({
#                 "success": True,
#                 "message": "Payment retrieved successfully",
#                 "data": {
#                     "email": customer.email,
#                     "amount_total": session.amount_total / 100,  # Stripe amount is in cents
#                     "currency": session.currency.upper(),
#                     "payment_status": session.payment_status,
#                     "session_id": session.id
#                 }
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             raise ParseError(f"An error occurred: {str(e)}") 


    

# from rest_framework.permissions import AllowAny

# class StripeSuccessApiView(views.APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         session_id = request.query_params.get("session_id")

#         if not session_id:
#             return Response({"error": "Missing session_id"}, status=400)

#         try:
#             session = stripe.checkout.Session.retrieve(session_id)
#             customer = stripe.Customer.retrieve(session.customer)

#             PaymentModel.objects.create(
#                 order_id=session.metadata.get("order_id"),
#                 user_id=session.metadata.get("user_id"),
#                 amount=session.amount_total / 100,
#                 currency=session.currency.upper(),
#                 payment_status=session.payment_status,
#                 stripe_session_id=session.id
#             )

#             return Response({
#                 "success": True,
#                 "message": "Payment successful",
#                 "data": {
#                     "email": customer.email,
#                     "amount_total": session.amount_total / 100,
#                     "currency": session.currency.upper(),
#                     "payment_status": session.payment_status,
#                     "session_id": session.id
#                 }
#             }, status=200)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)


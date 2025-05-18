import stripe
import logging

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import  views 
from rest_framework import  status 
from rest_framework import  permissions


from django.contrib.auth import get_user_model
from decouple import config


from xApiCart.models import OrderModel 
from common.xpaymentprocessor import PaymentProcessor 


from .models import PaymentModel
from .serializers import PaymentSerializer 

stripe.api_key = config("STRIPE_TEST_SECRET_KEY")

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
        



class StripeCancelApiView(views.APIView):
    def get(self, request):
        return Response({"message": "Payment was cancelled."}, status=status.HTTP_200_OK)
    




logger = logging.getLogger(__name__)

class StripeSuccessApiView(APIView):
    permission_classes = []

    def get(self, request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"error": "Missing session_id"}, status=400)
        try:
            session = stripe.checkout.Session.retrieve(session_id)

            session_data = session if isinstance(session, dict) else session.to_dict()
            successfull_payer_data = PaymentProcessor(session_data).get_payment_data() 


            PaymentModel.objects.create(
                order_id=successfull_payer_data.get("order_id"), 
                user_id=successfull_payer_data.get("user_id"), 
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


            return Response(successfull_payer_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Stripe session retrieve error: %s", str(e))
            return Response({"error": str(e)}, status=500)
        except stripe.error.StripeError as e:
            logger.error("Stripe error: %s", str(e))
            return Response({"error": "Stripe error occurred."}, status=500)
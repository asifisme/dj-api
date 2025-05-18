
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from decouple import config
import stripe
import logging

from .models import PaymentModel
from .serializers import PaymentSerializer
from xApiCart.models import OrderModel

# Stripe API Key (test or live)
stripe.api_key = config("STRIPE_TEST_SECRET_KEY")

# User model
User = get_user_model()

# Logger
logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['post'], url_path='create-checkout-session')
    def create_checkout_session(self, request):
        try:
            data = request.data

            # Retrieve order ID
            order_id = data.get('order_id')
            if not order_id:
                return Response({'error': 'order_id is required.'}, status=400)

            # Get the order
            try:
                order = OrderModel.objects.get(id=order_id)
            except OrderModel.DoesNotExist:
                return Response({'error': 'Order not found.'}, status=404)

            # Use authenticated user or fallback
            user = request.user if request.user.is_authenticated else order.user

            # Create Stripe checkout session
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
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )

            # Optional: retrieve payment intent
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

            # Save payment info
            payment = PaymentModel.objects.create(
                order=order,
                user=user,
                amount_paid=payment_intent.amount_received // 100 if payment_intent.amount_received else None,
                currency=payment_intent.currency,
                stripe_checkout_id=session.id,
                stripe_payment_intent=payment_intent.id,
                stripe_payment_status=payment_intent.status,
                stripe_payment_method=payment_intent.payment_method,
                receipt_url=payment_intent.charges.data[0].receipt_url if payment_intent.charges.data else None
            )

            # Return the checkout session URL to frontend
            return Response({"checkout_url": session.url}, status=200)

        except stripe.error.StripeError as e:
            logger.error("Stripe error: %s", str(e), exc_info=True)
            return Response({"error": "Stripe error occurred."}, status=500)

        except Exception as e:
            logger.error("Unexpected error: %s", str(e), exc_info=True)
            return Response({"error": "Unexpected server error."}, status=500)



# import stripe
# from decouple import config

# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from .models import PaymentModel
# from .serializers import PaymentSerializer
# from xApiCart.models import OrderModel

# from django.contrib.auth import get_user_model
# User = get_user_model()

# import logging
# logger = logging.getLogger(__name__)

# stripe.api_key = config("STRIPE_TEST_SECRET_KEY")

# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = PaymentModel.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.AllowAny]
#     http_method_names = ['get', 'post']

#     @action(detail=False, methods=['post'], url_path='create-checkout-session')
#     def create_checkout_session(self, request):
#         try:
#             # Extract order_id from request
#             order_id = request.data.get('order_id')
#             if not order_id:
#                 return Response({'error': 'order_id is required.'}, status=400)

#             try:
#                 order = OrderModel.objects.get(id=order_id)
#             except OrderModel.DoesNotExist:
#                 return Response({'error': 'Order not found.'}, status=404)

#             # Use request.user or a default user (depending on your auth system)
#             user = request.user if request.user.is_authenticated else order.user

#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'usd',
#                         'product_data': {
#                             'name': f'Order #{order_id}',
#                         },
#                         'unit_amount': int(order.total_amount * 100),  # Assuming your model has total_price
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/success/'),
#                 cancel_url=request.build_absolute_uri('/cancel/'),
#             )

#             # Get payment intent details
#             payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

#             # Save to DB
#             payment = PaymentModel.objects.create(
#                 order=order,
#                 user=user,
#                 amount_paid=payment_intent.amount_received // 100 if payment_intent.amount_received else None,
#                 currency=payment_intent.currency,
#                 stripe_checkout_id=session.id,
#                 stripe_payment_intent=payment_intent.id,
#                 stripe_payment_status=payment_intent.status,
#                 stripe_payment_method=payment_intent.payment_method,
#                 receipt_url=payment_intent.charges.data[0].receipt_url if payment_intent.charges.data else None
#             )

#             return Response({"sessionId": session.id}, status=200)

#         except Exception as e:
#             logger.error("Stripe checkout session creation failed", exc_info=True)
#             return Response({"error": str(e)}, status=500)



# import stripe
# import logging

# from decouple import config
# from django.contrib.auth import get_user_model

# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.exceptions import ParseError

# from .models import PaymentModel
# from .serializers import PaymentSerializer
# from xApiCart.models import OrderModel

# # Configure logging
# logger = logging.getLogger(__name__)

# # Stripe API key
# stripe.api_key = config("STRIPE_TEST_SECRET_KEY")

# # User model
# User = get_user_model()

# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = PaymentModel.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.AllowAny]
#     http_method_names = ['get', 'post']

#     @action(detail=False, methods=['post'], url_path='create-checkout-session')
#     def create_checkout_session(self, request):
#         try:
#             try:
#                 data = request.data
#             except ParseError:
#                 return Response({'error': 'Malformed JSON. Please check your request body.'}, status=400)

#             # Get order_id from request
#             order_id = data.get('order_id')
#             if not order_id:
#                 return Response({'error': 'order_id is required.'}, status=400)

#             # Retrieve the order
#             try:
#                 order = OrderModel.objects.get(id=order_id)
#             except OrderModel.DoesNotExist:
#                 return Response({'error': 'Order not found.'}, status=404)

#             # Get the user (authenticated or fallback to order.user)
#             user = request.user if request.user.is_authenticated else order.user

#             # Create Stripe Checkout Session
#             try:
#                 session = stripe.checkout.Session.create(
#                     payment_method_types=['card'],
#                     line_items=[{
#                         'price_data': {
#                             'currency': 'usd',
#                             'product_data': {
#                                 'name': f'Order #{order_id}',
#                             },
#                             'unit_amount': int(order.total_amount * 100),  # Convert to cents
#                         },
#                         'quantity': 1,
#                     }],
#                     mode='payment',
#                     success_url=request.build_absolute_uri('/success/'),
#                     cancel_url=request.build_absolute_uri('/cancel/'),
#                 )
#             except stripe.error.StripeError as e:
#                 logger.error("Stripe session creation failed: %s", str(e), exc_info=True)
#                 return Response({"error": "Failed to create Stripe Checkout session."}, status=500)

#             # Retrieve payment intent (optional, but used here)
#             try:
#                 payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
#             except stripe.error.StripeError as e:
#                 logger.error("Failed to retrieve payment intent: %s", str(e), exc_info=True)
#                 return Response({"error": "Failed to retrieve payment intent."}, status=500)

#             # Save payment details to the database
#             payment = PaymentModel.objects.create(
#                 order=order,
#                 user=user,
#                 amount_paid=payment_intent.amount_received // 100 if payment_intent.amount_received else None,
#                 currency=payment_intent.currency,
#                 stripe_checkout_id=session.id,
#                 stripe_payment_intent=payment_intent.id,
#                 stripe_payment_status=payment_intent.status,
#                 stripe_payment_method=payment_intent.payment_method,
#                 receipt_url=payment_intent.charges.data[0].receipt_url if payment_intent.charges.data else None
#             )

#             return Response({"sessionId": session.id}, status=200)

#         except Exception as e:
#             logger.error("Unexpected error during checkout session creation", exc_info=True)
#             return Response({"error": "An unexpected error occurred. Please try again later."}, status=500)

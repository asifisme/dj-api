from django.apps import AppConfig


class XapipaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payment'
    label = "xApiPayment"  # This label is used to avoid conflicts with other apps 

    def ready(self):
        import Payment.signals 
from django.apps import AppConfig


class XapipaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xApiPayment'

    def ready(self):
        import xApiPayment.signals 
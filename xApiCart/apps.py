from django.apps import AppConfig


class XapicartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xApiCart'

    def ready(self):
        import xApiCart.signals 
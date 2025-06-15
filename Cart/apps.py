from django.apps import AppConfig


class XapicartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cart'
    label = "xApiCart"  # This label is used to avoid conflicts with other apps 

    def ready(self):
        import Cart.signals 
from django.apps import AppConfig


class XapiproductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Product'
    label = "xApiProduct"  # This label is used to avoid conflicts with other apps 

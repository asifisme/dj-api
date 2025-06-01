from django.apps import AppConfig


class XapiauthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Authentication'
    label = "xApiAuthentication"  # This label is used to avoid conflicts with other apps 

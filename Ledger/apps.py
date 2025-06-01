from django.apps import AppConfig


class XapiledgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ledger'
    label = "xApiLedger"  # This label is used to avoid conflicts with other apps 

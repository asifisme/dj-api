from django.apps import AppConfig


class XapiarticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Article'
    label = "xApiArticle"  # This label is used to avoid conflicts with other apps

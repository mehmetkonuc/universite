from django.apps import AppConfig


class LikesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.likes'

    def ready(self):
        import apps.likes.signals  # Sinyalleri import ediyoruz
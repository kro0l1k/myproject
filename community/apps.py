from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "community"
    verbose_name = "Community Platform"

    def ready(self):
        """Initialize app and register signals."""
        pass  # Import signals here when needed

from django.apps import AppConfig
from asgiref.sync import sync_to_async


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        from scrapers import updater
        updater.start_scheduler()

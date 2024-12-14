from django.apps import AppConfig


class TestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testapp'
    def ready(self):
        from .tasks import start_scheduler
        start_scheduler()
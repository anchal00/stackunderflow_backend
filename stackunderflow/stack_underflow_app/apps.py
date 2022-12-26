from django.apps import AppConfig


class StackUnderflowAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stack_underflow_app"

    def ready(self):
        import stack_underflow_app.signals

        # Silence flake8 "unused import" error
        assert stack_underflow_app.signals

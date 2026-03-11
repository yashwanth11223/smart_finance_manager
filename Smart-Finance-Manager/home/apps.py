from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    
    def ready(self):
        """
        Called when Django app is ready.
        Import signals here to register signal handlers for automatic 
        UserProfile and UserExpenseAccount creation.
        """
        import home.signals  # noqa

from django.apps import AppConfig

class BussappConfig(AppConfig):
    name = 'bussapp'

    def ready(self):
        import bussapp.signals  # Import signals to connect them

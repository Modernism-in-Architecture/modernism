from django.apps import AppConfig


class MiaBuildingsConfig(AppConfig):
    name = "mia_buildings"

    def ready(self):
        import mia_buildings.signals

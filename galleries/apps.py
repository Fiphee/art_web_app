from django.apps import AppConfig


class GalleriesConfig(AppConfig):
    name = 'galleries'

    def ready(self):
        import galleries.signals
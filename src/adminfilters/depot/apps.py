from django.apps import AppConfig


class Config(AppConfig):
    name = 'adminfilters.depot'

    def ready(self):
        pass
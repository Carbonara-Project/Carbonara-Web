from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .lshforest import create_lshforest_tables

class ApiConfig(AppConfig):
    name = 'api'
    
    def ready(self):
        #execute raw sql after migrations
        post_migrate.connect(create_lshforest_tables, sender=self)

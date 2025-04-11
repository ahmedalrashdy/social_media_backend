from django.apps import AppConfig


class UtilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utils'
    
    
    def ready(self):
        from . import redis_client
        redis_client.initialize_redis()
        return super().ready()

from django.apps import AppConfig


class SocialNetworkMessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_network_messages'

    def ready(self):
        from social_network_messages.scheduler import updater
        updater.start()

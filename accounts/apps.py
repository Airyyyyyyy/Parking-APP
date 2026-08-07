from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # djongo mishandles `save(update_fields=[...])`, which Django's built-in
        # `update_last_login` receiver uses on every login. Disconnect it so
        # logging in doesn't crash. We only lose the `last_login` timestamp.
        from django.contrib.auth.signals import user_logged_in
        from django.contrib.auth.models import update_last_login
        # Django connects this with dispatch_uid="update_last_login"; the
        # disconnect must pass the same uid or it silently does nothing.
        user_logged_in.disconnect(update_last_login, dispatch_uid="update_last_login")

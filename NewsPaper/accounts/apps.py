from django.apps import AppConfig


# Обозначаем некоторые настройки по умолчанию
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

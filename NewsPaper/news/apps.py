from django.apps import AppConfig


# Обозначаем некоторые настройки по умолчанию
class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # Подключаем сигналы к Config проекта
    def ready(self):
        import news.signals


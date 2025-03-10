from ..models import Post
from datetime import timedelta, datetime
from django.utils import timezone

class Generator:

    def __init__(self, start_date=None, end_date=None):
        if end_date:
            self.end_date = self.get_my_timezone_date(end_date)
        else:
            self.end_date = timezone.now().date()

        if start_date:
            self.start_date = self.get_my_timezone_date(start_date)
        else:
            self.start_date = self.end_date - timedelta(days=7)

    @staticmethod
    def get_my_timezone_date(original_datetime):
        new_datetime = datetime.strptime(original_datetime, '%Y-%m-%d')
        tz = timezone.get_current_timezone()
        time_zone_datetime = timezone.make_aware(new_datetime, tz, True)
        return time_zone_datetime.date()

    def get_query(self):
        url_post = f'http://127.0.0.1:8000{'/news/'}'
        query = Post.objects.filter(
            time_in_post__gte=self.start_date,
            time_in_post__lt=self.end_date
        ).values_list('title_post', 'category_post').all()
        query = [{'username_user': 'Игорь',
                  'email_user': 'iv@rossvik.moscow',
                  'categories': [
                      {'name_category': 'Свежее',
                       'list_posts': [{'title_post': '«Химки» — это просто набор футболистов. У них нет, не было и не будет никакой выстроенной игры» — Генич.',
                                       'url_post': url_post},
                                      {'title_post': '«Тестовое второе сообщение.',
                                       'url_post': url_post}
                                      ]},
                      {'name_category': 'Культура',
                       'list_posts': [{'title_post': '«Культурная статья для примера.',
                                       'url_post': url_post},
                                      {'title_post': '«Вторая культурная статься для тестовой отправки.',
                                       'url_post': url_post}
                                      ]}]},
                 {'username_user': 'Света',
                  'email_user': 'file-sv@yandex.ru',
                  'categories': [
                      {'name_category': 'Популярное',
                       'list_posts': [{
                                          'title_post': '«Химки» — это просто набор футболистов. У них нет, не было и не будет никакой выстроенной игры» — Генич.',
                                          'url_post': url_post},
                                      {'title_post': '«Тестовое второе сообщение.',
                                       'url_post': url_post}
                                      ]},
                      {'name_category': 'Шоу-Бизнес',
                       'list_posts': [{'title_post': '«Культурная статья для примера.',
                                       'url_post': url_post},
                                      {'title_post': '«Вторая культурная статься для тестовой отправки.',
                                       'url_post': url_post}
                                      ]}]},
                 ]
        return query

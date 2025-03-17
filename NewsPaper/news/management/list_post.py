from django.contrib.auth.models import User
from ..models import Post, Category
from datetime import timedelta, datetime
from django.utils import timezone

class Generator:

    def __init__(self, start_date=None, end_date=None):
        if end_date:
            self.end_date = self.get_my_timezone_date(end_date)
        else:
            self.end_date = timezone.now().date() + timedelta(days=1)

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

    def get_dict_subscribers(self):
        dict_category = {
            'NEW': 'Свежее',
            'POP': 'Популярное',
            'INC': 'Происшествия',
            'SPO': 'Спорт',
            'SHB': 'Шоу-бизнес',
            'INT': 'Интернет',
            'CAR': 'Автомобили',
            'CUL': 'Культура',
            'POL': 'Политика',
            'SOC': 'Общество',
            'TEC': 'Наука и технологии',
            'ECN': 'Экономика',
            'REL': 'Религия',
            'WIL': 'Живая природа',
            'ECO': 'Экология',
        }
        dict_subscribers = {}
        subscribers = set(Category.objects.values_list('pk', 'subscribers').all())
        for subscriber in subscribers:
            if subscriber[1] is not None:
                try:
                    list_posts = list(Post.objects.filter(
                        category_post=subscriber[0],
                        time_in_post__gte=self.start_date,
                        time_in_post__lt=self.end_date
                    ).values('title_post', 'pk').all())
                    if len(list_posts) > 0:
                        dict_subscribers[subscriber[1]]['categories'].append(
                            {'name_category': dict_category[Category.objects.get(pk=subscriber[0]).name_category],
                             'list_posts': list_posts})
                except KeyError:
                    list_posts = list(Post.objects.filter(
                                            category_post=subscriber[0],
                                            time_in_post__gte=self.start_date,
                                            time_in_post__lt=self.end_date
                                        ).values('title_post', 'pk').all())
                    if len(list_posts) > 0:
                        dict_subscribers[subscriber[1]] = {
                            'categories': [{'name_category': dict_category[Category.objects.get(pk=subscriber[0]).name_category],
                                            'list_posts': list_posts}]}
        return dict_subscribers

    def get_query(self):
        dict_with_data = self.get_dict_subscribers()
        query = []
        for current_user, category in dict_with_data.items():
            user = User.objects.get(pk=current_user)
            query.append({'username_user': user.username,
                          'email_user': user.email,
                          'categories': category['categories']})
        return query

import locale
from django.forms import CheckboxSelectMultiple, TextInput, DateInput
from django_filters import FilterSet, CharFilter, DateFilter, MultipleChoiceFilter
from .models import Post, Author, User

locale.setlocale(category=locale.LC_ALL, locale="ru_RU.utf8")

class MyDateInput(DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class PostFilter(FilterSet):
    Author = MultipleChoiceFilter(label='Автор контента:',
                                  field_name='author_post',
                                  choices=[(n[0], User.objects.get(pk=n[1]).username) for n in Author.objects.exclude(user=8).values_list('id', 'user')],
                                  required=False,
                                  widget=CheckboxSelectMultiple(attrs={'class': 'author-checkbox'}))
    Title = CharFilter(label='Заголовок содержит:',
                       field_name='title_post',
                       lookup_expr='icontains',
                       widget=TextInput(attrs={'class': 'title-input'}))
    TextPost = CharFilter(label='Текст содержит:',
                          field_name='text_post',
                          lookup_expr='icontains',
                          widget=TextInput(attrs={'class': 'text-input'}))
    DateLt = DateFilter(label='Дата меньше:',
                        field_name='time_in_post',
                        lookup_expr='lt',
                        widget=MyDateInput(attrs={'class': 'date-lt-input'}))
    DateGt = DateFilter(label='Дата больше:',
                        field_name='time_in_post',
                        lookup_expr='gt',
                        widget=MyDateInput(attrs={'class': 'date-gt-input'}))
    class Meta:
        model = Post
        fields = [
           'title_post',
           'text_post',
           'time_in_post',
           'author_post',
       ]
        exclude = [
            'title_post',
            'text_post',
            'time_in_post',
            'author_post'
        ]
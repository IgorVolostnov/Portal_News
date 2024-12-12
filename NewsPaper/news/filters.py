import datetime
import locale
from django.forms import CheckboxSelectMultiple, TextInput, SelectDateWidget, DateInput
from django_filters import FilterSet, CharFilter, DateFilter, MultipleChoiceFilter
from .models import Post

locale.setlocale(category=locale.LC_ALL, locale="Russian")

class MyDateInput(DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class PostFilter(FilterSet):
    TypePost = MultipleChoiceFilter(label='Вид контента:', field_name='type_post', choices=Post.KIND_CONTENT,
                                    widget=CheckboxSelectMultiple(attrs={'class': 'category-checkbox'}))
    Title = CharFilter(label='Заголовок содержит:', field_name='title_post', lookup_expr='icontains',
                       widget=TextInput(attrs={'class': 'title-input'}))
    TextPost = CharFilter(label='Текст содержит:', field_name='text_post', lookup_expr='icontains',
                          widget=TextInput(attrs={'class': 'text-input'}))
    DateLt = DateFilter(label='Дата меньше:', field_name='time_in_post', lookup_expr='lt',
                        widget=MyDateInput(attrs={'class': 'date-lt-input'}))
    DateGt = DateFilter(label='Дата больше:', field_name='time_in_post', lookup_expr='gt',
                        widget=MyDateInput(attrs={'class': 'date-gt-input'}))
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author_post', 'type_post', 'time_in_post', 'category_post', 'title_post', 'text_post', 'rating_post']

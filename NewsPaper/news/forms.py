import locale
from django import forms
from django.core.exceptions import ValidationError
from django.forms import CharField, Textarea, RadioSelect
from django_filters.fields import ModelChoiceField

from .models import Post, Author

locale.setlocale(category=locale.LC_ALL, locale="ru_RU.utf8")

# Создаем свой класс на основании ModelChoiceField для отображения username авторов контента
class MyModelChoiceFieldAuthor(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.user.username}"

class PostForm(forms.ModelForm):
    author_post = MyModelChoiceFieldAuthor(label='Автор контента:',
                                           queryset=Author.objects.exclude(user=8),
                                           widget=RadioSelect(attrs={'class': 'form-author-checkbox'}))
    title_post = CharField(label='Заголовок контента:',
                           max_length=500,
                           widget=Textarea(attrs={'class': 'form-title-input'}))
    text_post = CharField(label='Текст контента:',
                          widget=Textarea(attrs={'class': 'form-text-input'}))
    class Meta:
        model = Post
        fields = [
            'author_post',
            'title_post',
            'text_post',
        ]

    # Проверка полей формы, если необходимо
    def clean(self):
        cleaned_data = super().clean()
        title_post = cleaned_data.get("title_post")
        text_post = cleaned_data.get("text_post")
        if title_post == text_post:
            raise ValidationError(
               "Описание не должно быть идентично названию."
            )
        return cleaned_data
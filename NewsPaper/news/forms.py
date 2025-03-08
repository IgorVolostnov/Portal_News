import locale
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.forms import CharField, Textarea, RadioSelect, ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField
from django.template.loader import render_to_string
from django_filters.fields import ModelChoiceField
from .models import Post, Author, Category


locale.setlocale(category=locale.LC_ALL, locale="ru_RU.utf8")

# Создаем свой класс на основании ModelChoiceField для отображения username авторов контента
class MyModelChoiceFieldAuthor(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.user.username}"

class MyModelChoiceFieldCategory(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj}"

class PostForm(ModelForm):
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
    author_post = MyModelChoiceFieldAuthor(label='Автор контента:',
                                           queryset=Author.objects.exclude(user=8),
                                           widget=RadioSelect(attrs={'class': 'form-author-checkbox'}))
    category_post = MyModelChoiceFieldCategory(label='Категория контента:',
                                             queryset=Category.objects.all(),
                                             widget=CheckboxSelectMultiple(attrs={'class': 'form-category-checkbox'}))
    title_post = CharField(label='Заголовок контента:',
                           max_length=500,
                           widget=Textarea(attrs={'class': 'form-title-input'}))
    text_post = CharField(label='Текст контента:',
                          widget=Textarea(attrs={'class': 'form-text-input'}))
    class Meta:
        model = Post
        fields = [
            'author_post',
            'category_post',
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
        subscribers = set(cleaned_data.get("category_post").values_list('name_category', 'subscribers').all())
        dict_subscribers = {}
        for subscriber in subscribers:
            if subscriber[1] is not None:
                current_user = User.objects.get(pk=subscriber[1])
                try:
                    dict_subscribers[self.dict_category[subscriber[0]]][current_user.email] = current_user.username
                except KeyError:
                    dict_subscribers[self.dict_category[subscriber[0]]] = {current_user.email: current_user.username}
        print(dict_subscribers)
        for item in dict_subscribers.values():
            for email_user, username_user in item.items():
                # Получаем наш html-макет
                html_content = render_to_string(
                    'category_mail.html',
                    {
                        'user_name': username_user,
                        'text_title': title_post,
                        'text_content': text_post,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {username_user}. Новая статья в твоём любимом разделе!',
                    body=text_post,  # это то же, что и message
                    to=[email_user],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем
        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
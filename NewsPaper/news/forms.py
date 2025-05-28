import locale
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import CharField, Textarea, RadioSelect, ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField, \
    FileField, ClearableFileInput, inlineformset_factory
from django_filters.fields import ModelChoiceField
from .models import Post, Author, Category, PostImage

locale.setlocale(category=locale.LC_ALL, locale="ru_RU.utf8")

# Создаем свой класс на основании ModelChoiceField для отображения username авторов контента
class MyModelChoiceFieldAuthor(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.user.username}"


# Создаем свой класс на основании ModelMultipleChoiceField для отображения названия категорий контента
class MyModelChoiceFieldCategory(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj}"


# Форма для создания и изменения модели Post
class PostForm(ModelForm):
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
        return cleaned_data


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ImageForm(ModelForm):
    images = MultipleFileField()

    class Meta:
        model = PostImage
        fields = ('images', )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ImageForm, self).__init__(*args, **kwargs)


PostImageFormSet = inlineformset_factory(parent_model=Post, model=PostImage, form=ImageForm, fields=['images'], extra=1)


# Переопределяем форму регистрации, для добавления пользователя в группу common
class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
import datetime
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group, User
from .models import Post, SubscribersCategory, PostImage
from .filters import PostFilter
from .forms import PostForm, PostImageFormSet
from .tasks import mail_to_subscribers
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .validators import validate_is_image


# Представление списка новостей и статей в зависимости от категории
class CategoryNewsList(ListView):
    model = Post
    ordering = '-time_in_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем queryset, для получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset().filter(category_post=self.kwargs['value'])
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        user_me = self.request.user
        category_me = self.kwargs['value']
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        if user_me.id is not None:
            context['is_not_subscribers'] = not SubscribersCategory.objects.filter(
                subscribers_id=int(user_me.id),
                category_id=int(category_me)
            ).exists()
        context['category_id'] = category_me
        context['time_now'] = datetime.datetime.now(datetime.timezone.utc)
        context['next_news'] = f"Свежие новости на {datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')}: "
        context['type_content'] = "НОВОСТИ"
        context['filterset'] = self.filterset
        return context

# Представление списка новостей и статей в зависимости от категории для пользователя, который подписался на категорию
class Subscribers(ListView):
    model = Post
    ordering = '-time_in_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем queryset, для получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset().filter(category_post=self.kwargs['value'])
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        user_me = self.request.user
        category_me = self.kwargs['value']
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        if user_me.id is not None:
            user_current = User.objects.get(pk=user_me.id)
            if not SubscribersCategory.objects.filter(
                    subscribers_id=int(user_me.id),
                    category_id=int(category_me)
            ).exists():
                SubscribersCategory.objects.create(
                    subscribers=user_current,
                    category_id=int(category_me),
                )
            else:
                print('Пользователь уже подписан')
        context['is_not_subscribers'] = not SubscribersCategory.objects.filter(
            subscribers_id=int(user_me.id),
            category_id=int(category_me)
        ).exists()
        context['category_id'] = category_me
        context['time_now'] = datetime.datetime.now(datetime.timezone.utc)
        context['next_news'] = f"Свежие новости на {datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')}: "
        context['type_content'] = "НОВОСТИ"
        context['filterset'] = self.filterset
        return context


# Представление списка новостей
class NewsList(ListView):
    model = Post
    ordering = '-time_in_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем queryset, для получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset().filter(type_post='NE')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['time_now'] = datetime.datetime.now(datetime.timezone.utc)
        context['next_news'] = f"Свежие новости на {datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')}: "
        context['type_content'] = "НОВОСТИ"
        context['filterset'] = self.filterset
        return context


# Представление списка статей
class ArticlesList(ListView):
    model = Post
    ordering = '-time_in_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем queryset, для получения списка статей
    def get_queryset(self):
        queryset = super().get_queryset().filter(type_post='AR')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['time_now'] = datetime.datetime.now(datetime.timezone.utc)
        context['next_news'] = f"Свежие новости на {datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')}: "
        context['type_content'] = "СТАТЬИ"
        context['filterset'] = self.filterset
        return context


# Детальное представление новостей и статей
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_images'] = [obj.images.url for obj in self.object.photos.all()]
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['skip_column'] = "     "
        return context

    # Добавляем объект в кэш пока он не изменится
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


# Представление для создания новостей
class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.request.FILES.getlist('photos-0-images', None)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['type_content'] = "НОВОСТИ"
        context['create_content'] = "НОВАЯ НОВОСТЬ"
        if self.request.POST:
            context['form_images'] = PostImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form_images'] = PostImageFormSet()
        return context

    # При создании новости заполняем поле тип контента значением 'NE'
    def form_valid(self, form):
        context = self.get_context_data()
        form_images = context['form_images']
        photos = context['gallery']
        with transaction.atomic():
            if form_images.is_valid():
                self.object = form.save(commit=False)
                self.object.type_post = 'NE'
                self.object.save()
                form_images.instance = self.object
                for photo in photos:
                    if validate_is_image(photo):
                        self.object.photos.create(images=photo)
            mail_to_subscribers.delay(self.object.pk)
        return super().form_valid(form)


# Представление для создания статей
class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.request.FILES.getlist('photos-0-images', None)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['type_content'] = "СТАТЬИ"
        context['create_content'] = "НОВАЯ СТАТЬЯ"
        if self.request.POST:
            context['form_images'] = PostImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form_images'] = PostImageFormSet()
        return context

    # При создании статьи заполняем поле тип контента значением 'AR'
    def form_valid(self, form):
        context = self.get_context_data()
        form_images = context['form_images']
        photos = context['gallery']
        with transaction.atomic():
            if form_images.is_valid():
                self.object = form.save(commit=False)
                self.object.type_post = 'AR'
                self.object.save()
                form_images.instance = self.object
                for photo in photos:
                    if validate_is_image(photo):
                        self.object.photos.create(images=photo)
            mail_to_subscribers.delay(self.object.pk)
        return super().form_valid(form)

# Добавляем представление для изменения новости.
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['gallery'] = self.request.FILES.getlist('photos-0-images', None)
        context['post_images'] = [obj.images.url for obj in self.object.photos.all()]
        if len(context['post_images']) == 0:
            context['title_post_images'] = ''
        else:
            context['title_post_images'] = 'Уже загруженные изображения и видео:'
        context['type_content'] = "НОВОСТИ"
        context['create_content'] = "РЕДАКТИРОВАТЬ НОВОСТЬ"
        if self.request.POST:
            context['form_images'] = PostImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form_images'] = PostImageFormSet()
        return context

    # При изменении статьи
    def form_valid(self, form):
        context = self.get_context_data()
        form_images = context['form_images']
        photos = context['gallery']
        with transaction.atomic():
            if form_images.is_valid():
                self.object = form.save(commit=False)
                self.object.type_post = 'NE'
                self.object.save()
                form_images.instance = self.object
                for photo in photos:
                    if validate_is_image(photo):
                        self.object.photos.create(images=photo)
            mail_to_subscribers.delay(self.object.pk)
        return super().form_valid(form)


# Добавляем представление для изменения статьи.
class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['gallery'] = self.request.FILES.getlist('photos-0-images', None)
        context['post_images'] = [obj.images.url for obj in self.object.photos.all()]
        if len(context['post_images']) == 0:
            context['title_post_images'] = ''
        else:
            context['title_post_images'] = 'Уже загруженные изображения и видео:'
        context['type_content'] = "СТАТЬИ"
        context['create_content'] = "РЕДАКТИРОВАТЬ СТАТЬЮ"
        if self.request.POST:
            context['form_images'] = PostImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form_images'] = PostImageFormSet()
        return context

    # При изменении статьи
    def form_valid(self, form):
        context = self.get_context_data()
        form_images = context['form_images']
        photos = context['gallery']
        with transaction.atomic():
            if form_images.is_valid():
                self.object = form.save(commit=False)
                self.object.type_post = 'AR'
                self.object.save()
                form_images.instance = self.object
                for photo in photos:
                    if validate_is_image(photo):
                        self.object.photos.create(images=photo)
            mail_to_subscribers.delay(self.object.pk)
        return super().form_valid(form)

# Представление удаляющее новость.
class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['type_content'] = "НОВОСТИ"
        context['create_content'] = "УДАЛИТЬ НОВОСТЬ"
        return context

# Представление удаляющее статью.
class ArticlesDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles_list')

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['type_content'] = "СТАТЬИ"
        context['create_content'] = "УДАЛИТЬ СТАТЬЮ"
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


@cache_page(60)
def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': f'К сожалению такая страница была не найдена, или перемещена.',
    })


@cache_page(60)
def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': f'Внутренняя ошибка сайта, вернитесь на главную страницу, '
                         f'отчет об ошибке мы направим администрации сайта',
    })


@cache_page(60)
def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request=request, template_name='errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': f'Доступ к этой странице ограничен: {exception}',

    })
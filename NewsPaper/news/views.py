import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


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

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skip_column'] = "     "
        return context


# Представление для создания новостей
class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_content'] = "НОВОСТИ"
        context['create_content'] = "НОВАЯ НОВОСТЬ"
        return context

    # При создании новости заполняем поле тип контента значением 'NE'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'NE'
        return super().form_valid(form)

# Представление для создания статей
class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_content'] = "СТАТЬИ"
        context['create_content'] = "НОВАЯ СТАТЬЯ"
        return context

    # При создании статьи заполняем поле тип контента значением 'AR'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'AR'
        return super().form_valid(form)
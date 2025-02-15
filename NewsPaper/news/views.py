import datetime
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm, CustomSignupForm
from .token import account_activation_token
from django.core.mail import EmailMessage


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
class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

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
class ArticlesCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

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

# Добавляем представление для изменения новости.
class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_content'] = "НОВОСТИ"
        context['create_content'] = "РЕДАКТИРОВАТЬ НОВОСТЬ"
        return context


# Добавляем представление для изменения новости.
class ArticlesUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_content'] = "СТАТЬИ"
        context['create_content'] = "РЕДАКТИРОВАТЬ СТАТЬЮ"
        return context

# Представление удаляющее новость.
class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    # Добавляем дополнительный контекст, если нужно
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['type_content'] = "СТАТЬИ"
        context['create_content'] = "УДАЛИТЬ СТАТЬЮ"
        return context

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomSignupForm()
    return render(request, 'account/signup.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
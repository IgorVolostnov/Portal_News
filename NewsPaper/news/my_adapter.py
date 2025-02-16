from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/news/'


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        print('Мой социал адаптер работает')
        user = super(MySocialAccountAdapter, self).save_user(request, sociallogin, form=None)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user
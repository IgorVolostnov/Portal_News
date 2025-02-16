from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/news/'


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(MySocialAccountAdapter, self).save_user(request, sociallogin, form=None)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
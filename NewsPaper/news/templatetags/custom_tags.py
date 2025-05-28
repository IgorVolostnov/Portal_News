import datetime
from django import template

# Создание тегов для HTML-файлов
register = template.Library()

@register.simple_tag()
def current_time(format_string='%b %d %Y'):
   return datetime.datetime.strftime(datetime.datetime.now(), format_string)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

@register.simple_tag()
def first_image(post: object):
    photo = post.photos.first()
    if photo is None:
        photo = post.links.first()
        if photo is None:
            photo = 'https://www.rossvik.moscow/images/no_foto.png'
    else:
        list_split = str(photo).split("'")
        photo = list_split[1]
    return photo
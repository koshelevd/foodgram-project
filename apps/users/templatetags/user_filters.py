"""Application 'users' filters."""
from django import template


from urllib.parse import urlencode

from django.urls import resolve, Resolver404

from apps.recipes.models import Favorite, Purchase, Follow

register = template.Library()


@register.simple_tag
def active_page(request, view_name):
    if not request:
        return ""
    try:
        return "nav__item_active" if resolve(request.path_info).url_name == view_name else ""
    except Resolver404:
        return ""

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()

@register.filter
def shopcounter(user):
    return Purchase.objects.filter(user=user).count()

@register.filter
def isfollowing(author, user):
    return Follow.objects.filter(author=author, user=user).exists()

@register.filter
def ispurchased(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()

@register.filter
def isfavorite(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()

@register.filter
def addclass(field, css):
    """Return class for input fields."""
    return field.as_widget(attrs={"class": css})


@register.filter
def as_p(text, css):
    """Return HTML markup for text."""
    return ''.join(list(map(lambda x: f'<p class="{css}">{x}</p>',
                            text.split('\n'))))

@register.filter
def intmap(value):

    return list(map(int, value))
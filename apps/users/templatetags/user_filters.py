"""Application 'users' filters."""
from django import template

from apps.api.models import Favorite
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()


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
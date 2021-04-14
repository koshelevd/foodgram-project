"""Application 'users' filters."""
from django import template

register = template.Library()


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
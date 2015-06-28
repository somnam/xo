from django.template import Library
from django.core.urlresolvers import reverse

register = Library()

@register.filter
def get_range(value, start=0):
    """
    Returns a list containing range made from given value.
    """
    return range(start,value+start)

@register.filter
def add_error_class(field):
    return 'has-error' if field.errors else ''

@register.filter
def nav_class(request, urls):
    return 'active' if request.path in (reverse(url) for url in urls.split()) else ''

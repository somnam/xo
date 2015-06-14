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
def is_even(value):
    """
    Returns true for even numeric values.
    """
    return False if value % 2 else True

@register.simple_tag
def nav_class(request, urls):
    nav_class = ''
    if request.path in ( reverse(url) for url in urls.split() ):
        nav_class = 'active'
    return nav_class

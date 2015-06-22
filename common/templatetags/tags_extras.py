from django.template import Library
from django.core.urlresolvers import reverse

register = Library()

@register.filter
def get_range(value, start=0):
    """
    Returns a list containing range made from given value.
    """
    return range(start,value+start)

@register.simple_tag
def nav_class(request, urls):
    return 'active' if request.path in (reverse(url) for url in urls.split()) else ''

@register.simple_tag
def form_group_class(field):
    classes = ['form-group']
    if field.errors: classes.append('has-error')
    return ' '.join(classes)

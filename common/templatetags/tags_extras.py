from django.template import Library

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

from django.template import Library

register = Library()

@register.filter
def get_range(value):
    """
    Returns a list containing range made from given value.
    """
    return range(value)

@register.filter
def is_even(value):
    """
    Returns true for even numeric values.
    """
    return 0 if value % 2 else 1

from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiply the arg and value"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

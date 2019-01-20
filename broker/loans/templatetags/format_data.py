from django import template

register = template.Library()

@register.filter(name='format_phone')
def format_phone(value):
    return '(' + value[0:3] + ')' + ' ' + value[3:6] + '-' + value[6:10]

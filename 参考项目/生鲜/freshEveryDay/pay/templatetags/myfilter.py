from django import template
register = template.Library()

@register.filter(name='mul')
def mul(price,count):
    sumPrice = price * count
    return sumPrice

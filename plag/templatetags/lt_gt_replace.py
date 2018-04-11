from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def rep(value):
    print("abc")
    return value.replace("&lt;","sample")#.replace("&lt;","<")
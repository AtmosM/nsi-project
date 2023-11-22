from django import template
from system.models import Documents


register = template.Library()

@register.simple_tag()
def documets_info():
    return Documents.objects.all()
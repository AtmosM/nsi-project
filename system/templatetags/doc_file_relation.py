from django import template
from system.models import RelationsDocuments


register = template.Library()

@register.simple_tag()
def docs_to_file():
    return RelationsDocuments.objects.all()
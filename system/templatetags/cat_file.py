from django import template
from system.models import Entities, Files, RelationsFiles
from system.views import category_detail

register = template.Library()

@register.simple_tag()
def current_category_files():
    return Files.objects.all()
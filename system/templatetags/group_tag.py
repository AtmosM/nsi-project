from django import template
from system.models import Entities, Files, RelationsFiles
from system.views import category_detail

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# @register.inclusion_tag('files_list.html')
# def show_files(sort=None):
#     files = Files.objects.all()
#     if RelationsFiles.id_file == Files.id and Entities.id == RelationsFiles.id_entities:
#         files = Files.objects.filter(id=RelationsFiles.id_file)
#         print(files)
#     return {'file': files}

@register.simple_tag()
def current_category_files():

    return Files.objects.all()


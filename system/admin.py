from django.contrib import admin

# Register your models here.

from .models import Entities, RelationsDocuments, Documents, Tags, Tag_Relation, Files, RelationsFiles # Comments, Users, User_groups, Group_access,
from django_mptt_admin.admin import DjangoMpttAdmin


class EntitiesAdmin(DjangoMpttAdmin):
    list_display = ('id', 'parent', 'ent_name', 'description')


admin.site.register(Entities, EntitiesAdmin)


class RelationsDocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_file', 'id_document')


admin.site.register(RelationsDocuments, RelationsDocumentsAdmin)


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'doc_name', 'doc_type', 'document', 'description', 'document_language')


admin.site.register(Documents, DocumentsAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')


admin.site.register(Tags, TagsAdmin)


class Tag_relationAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_tag', 'id_document', 'id_entity')


admin.site.register(Tag_Relation, Tag_relationAdmin)


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_version', 'add_data')


admin.site.register(Files, FilesAdmin)


# class CommentsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'id_document', 'id_user', 'comment', 'comment_date')
#
#
# admin.site.register(Comments, CommentsAdmin)
#
#
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user_name', 'user_password', 'password_hash')
#
#
# admin.site.register(Users, UsersAdmin)
#
#
# class User_groupsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'group_name', 'group_rights')
#
#
# admin.site.register(User_groups, User_groupsAdmin)
#
#
# class Group_accessAdmin(admin.ModelAdmin):
#     list_display = ('id', 'id_user_group', 'id_user')
#
#
# admin.site.register(Group_access, Group_accessAdmin)

class RelationsFilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_entities', 'id_file')

admin.site.register(RelationsFiles, RelationsFilesAdmin)
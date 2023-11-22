from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
import mptt
import uuid

def document_language_validator(document_language):
    """Проверка на валидность для выбранного языка докумнета"""
    if document_language not in ['0', '1']:
        raise ValidationError(
            gettext_lazy('%(document_language)s is not a valid language'),
            params={'document_language': document_language},
        )


class Documents(models.Model):
    """Модель таблицы для хранения документов"""
    class Meta:
        db_table = "documents"
        verbose_name = "Информация о документе"
        verbose_name_plural = "Информация о документе"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name='Уникальный идентификатор документа')
    doc_name = models.TextField(verbose_name='Название документа')
    doc_type = models.CharField(max_length=80, verbose_name="Тип документа")
    description = models.TextField(verbose_name='Описание документа')
    document_language = models.CharField(max_length=80, verbose_name='Язык докуменат')
    document = models.FileField(blank=True, null=True, upload_to='docs/', verbose_name='Документ')

    def get_html_document(self, object):
        if object.document:
            return mark_safe(f"<a href='{object.document.url}', width=400")
    def __str__(self):
        return f"{self.id} {self.doc_name} {self.document_language}"

    def get_absolute_url(self):
        return reverse('doc-files')




class Files(models.Model):
    """Модель таблицы для хранения информации о файлах."""
    class Meta:
        db_table = "files"
        verbose_name = "Информация о файлах"
        verbose_name_plural = "Информация о файлах"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, unique=True, verbose_name="Уникальный идентификатор файла")
    #id_document = models.ForeignKey(Documents, on_delete=models.RESTRICT, verbose_name='ID документа')
    file_name = models.CharField(max_length=50, unique=True, verbose_name="Имя файла")
    file = models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%D/', verbose_name='Файлы')
    file_version = models.CharField(max_length=20, verbose_name='Версия файла')
    add_data = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    slug = models.SlugField(unique=True, verbose_name='URL')

    def get_html_file(self, object):
        if object.file:
            return mark_safe(f"<a href='{object.file.url}', width=400")
    def __str__(self):
        return f"{self.id} {self.file_name} {self.file_version} {self.file} {self.slug}"

    # def get_absolute_url(self):
    #     return reverse('cat-files')

    def get_absolute_url(self):
        return reverse('cat-files', kwargs={'slug': self.slug})





class Entities(MPTTModel):
    """Древовидная модель таблицы категорий (сущностей)"""
    class Meta:
        db_table = "entities"
        verbose_name = "Сущности"
        verbose_name_plural = "Сущности"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, unique=True, verbose_name='Уникальный идентификатор сущности')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родитель сущности')
    ent_name = models.TextField(verbose_name='Имя сущности')
    description = models.TextField(verbose_name='Описание сущности')

    def get_absolute_url(self):
        return reverse('entitie-by-category', args=[str(self.id)])

    #mptt.register(Entities, order_insertion_by=['ent_name'])
    def __str__(self):
        return f"{self.id} {self.parent} {self.ent_name}"



# модель отношений
class RelationsDocuments(models.Model):
    """Модель таблицы для связи документов с файлами"""
    class Meta:
        db_table = "relations_documents"
        verbose_name = "Привязка документов к файлам"
        verbose_name_plural = "Привязка документов к файлам"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name='Уникальный идентивикатор отношения')
    id_file = models.ForeignKey(Files, on_delete=models.CASCADE, verbose_name='ID файла')
    id_document = models.ForeignKey(Documents, on_delete=models.CASCADE, verbose_name='ID документа')

    def __str__(self):
        return f"{self.id} {self.id_file} {self.id_document}"


class Tags(models.Model):
    """Модель таблицы для хранения и работы с тэгами"""
    class Meta:
        db_table = "tags"
        verbose_name = "Тэги"
        verbose_name_plural = "Тэги"

    id = models.UUIDField(primary_key=True, verbose_name='ID тэга')
    tag = models.CharField(max_length=20, unique=True, verbose_name='Тэг')

    def __str__(self):
        return f"{self.id} {self.tag}"



class Tag_Relation(models.Model):
    """Модель таблицы для хранения принадлежности тегов"""
    class Meta:
        db_table = "tags_relations"
        verbose_name = "Отношение тэгов"
        verbose_name_plural = "Отношение тэгов"

    id = models.UUIDField(primary_key=True, verbose_name="Уникальный идентификатор отношения тега")
    id_tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name='ID тэга')
    id_document = models.ForeignKey(Documents, on_delete=models.CASCADE, verbose_name='ID документа')
    id_entity = models.ForeignKey(Entities, on_delete=models.CASCADE, verbose_name='ID сущности')

    def __str__(self):
        return f"{self.id} {self.id_tag} {self.id_document} {self.id_entity}"



class RelationsFiles(models.Model):
    """Модель таблицы для связи файлов с категориями"""
    class Meta:
        db_table = 'relations_files'
        verbose_name = 'Отношения сущностей с файлами'
        verbose_name_plural = 'Отношения сущностей с файлами'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True,
                          verbose_name='Уникальный идентивикатор отношения')
    id_entities = models.ForeignKey(Entities, on_delete=models.CASCADE, verbose_name='ID категории')
    id_file = models.ForeignKey(Files, on_delete=models.CASCADE, verbose_name='ID файла')

    def __str__(self):
        return f"{self.id} {self.id_entities} {self.id_file}"


# валидация для прав доступа
def group_rights_validator(group_rights):
    if group_rights not in ['0', '1', '2', '3', '4']:
        raise ValidationError(
            gettext_lazy('%(group_rights)s is not a valid rights'),
            params={'group_rights': group_rights},
        )






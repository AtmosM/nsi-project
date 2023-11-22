from cProfile import label
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.shortcuts import redirect
from .models import Entities, Files, Documents, RelationsFiles, RelationsDocuments
import uuid
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.forms import ClearableFileInput, FileInput, SlugField
import logging

logger = logging.getLogger('main')
class EntitiesForm(forms.ModelForm):
    """Форма для внесения новых категорий в базу данных"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].empty_label = 'Родитель не выбран'
        

    class Meta:
        model = Entities
        fields=('parent','ent_name', 'description')

        widgets = {
            'ent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        

class DocumentsAddForm(forms.ModelForm):
    """Форма для добавления новых документов в дазу данных"""


    Language_choise = (
        ("Русский", "Русский"),
        ("Английский", "Английский"),

    )
    Type_choise = (
        ("ГОСТ", "ГОСТ"),
        ("Спецификация", "Спецификация"),
        ("Техническое задание", "Техническое задание")
    )

    document_language = forms.ChoiceField(choices=Language_choise)
    doc_type = forms.ChoiceField(choices=Type_choise)
    document = forms.FileField()
    class Meta:
        model = Documents
        fields = ('doc_name', 'document', 'doc_type', 'description', 'document_language')
        widgets = {
            'doc_name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            #'document': FileInput(),



        }

class FilesAddForm(forms.ModelForm):
    """Форма для добавления новых файлов в базу данных"""

    class Meta:
        model = Files
        fields = ('file_name', 'file', 'file_version', 'add_data')


        widgets ={
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
            'file_version': forms.TextInput(attrs={'class': 'form-control'}),
            'file': ClearableFileInput(attrs={'multiple': True}),



        }


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации новых пользователей"""
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email=forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    choice = (
        ("Нет доступа", "Нет доступа"),

    )
    default_group = forms.ChoiceField(widget=forms.RadioSelect, choices=choice)
    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('category-list')


class LoginUserForm(AuthenticationForm):
    """Форма для авторизации пользователей"""
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RelationFileForm(forms.ModelForm):
    """ Форма для привязки файлов к категории"""
    class Meta:

        model = RelationsFiles
        fields = ('id_entities', 'id_file')

class RelationDocumetnForm(forms.ModelForm):
    """ Форма для привязки файлов к категории"""
    class Meta:

        model = RelationsDocuments
        fields = ('id_file', 'id_document')



class DeleteCatForm(forms.ModelForm):
    """Форма удаления категории"""
    class Meta:
        model = Entities
        fields = '__all__'


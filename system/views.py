from _ast import Add
from xml.dom.minidom import Document

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.views.generic import ListView
from .models import Entities, Files, Documents
from .forms import EntitiesForm, DocumentsAddForm, FilesAddForm, RegisterUserForm, RelationFileForm, DeleteCatForm, RelationDocumetnForm
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
import logging
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View

# Create your views here.

# class EntitiesByCategoryView(ListView):
#     context_object_name = 'category_test'
#     template_name = 'post_list.html'
#
#     def get_queryset(self):
#         self.category = Entities.objects.get(self.kwargs)
#
#         return self.category
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['ent_name'] = self.category
#         return context

logger = logging.getLogger('main')

class Practice(TemplateView):
    template_name = 'pract.html'
class EntitiesListView(ListView):
    """
    A view that displays a list of all entities (categories).

    Attributes:
    -----------
    model : Model
        The model that the view will use to retrieve the data.
    template_name : str
        The name of the template that the view will use to render the data.

    Methods:
    --------
    get_queryset(self)
        Returns the queryset that the view will use to retrieve the data.

    get_context_data(self, **kwargs)
        Returns the context dictionary that the view will use to render the data.

    """
    model = Entities
    template_name = "base.html"


def category_detail(request, my_id):
    """
    Renders a category detail page with a list of all entities and additional information about the current category.

    Args:
        request (HttpRequest): The HTTP request object.
        my_id (int): The ID of the current category.

    Returns:
        HttpResponse: The HTTP response object containing the rendered category detail page.
    """

    nodes = Entities.objects.all()
    context = {
        'object_list': nodes,
        'current_category': Entities.objects.get(id=my_id),
        'root_category_id': Entities.objects.get(id=my_id).get_root().id,

    }

    return render(request, 'base.html', context=context)



class DocumentCreate(CreateView):
    """
    View for creating new documents.

    Attributes:
    -----------
    form_class : DocumentsAddForm
        The form class used for creating new documents.
    template_name : str
        The name of the template used for rendering the document creation form.
    success_url : str
        The URL to redirect to after successfully creating a new document.

    Methods:
    --------
    get(self, request, *args, **kwargs)
        Handles GET requests and returns a rendered document creation form.
    post(self, request, *args, **kwargs)
        Handles POST requests and creates a new document if the form is valid.

    Returns:
    --------
    A rendered document creation form or a redirect to the success URL.
    """
    logger.info("New document added")
    form_class = DocumentsAddForm
    template_name = 'document_create_form.html'
    success_url = reverse_lazy('doc-files')

class FileCreate(CreateView):
    """
    A class-based view for creating a new file.

    Args:
        form_class (Form): The form class to use for creating the file.
        template_name (str): The name of the template to render for the file creation form.
        success_url (str): The URL to redirect to upon successful file creation.

    Attributes:
        form_class (Form): The form class to use for creating the file.
        template_name (str): The name of the template to render for the file creation form.
        success_url (str): The URL to redirect to upon successful file creation.
    """
    logger.info("New file added")
    form_class = FilesAddForm
    template_name = 'file_create_form.html'
    success_url = reverse_lazy('cat-files')

#загрузка нескольких файлов одновременно
# def multiplay_files(request):
#     user = request.user
#     if request.method == 'POST':
#         form = MultFilesModelForm(request.POST)
#         file_form = FilesAddForm(request.POST, request.FILES)
#         files = request.FILES.getlist('file') #field name in model
#         if form.is_valid() and file_form.is_valid():
#             feed_instance = form.save(commit=False)
#             feed_instance.user = user
#             feed_instance.save()
#
#             for f in files:
#                 file_instance = Files(file=f, feed=feed_instance)
#                 file_instance.save()
#             return HttpResponseRedirect("/form")
#     else:
#         form = MultFilesModelForm()
#         file_form = FilesAddForm()
#
#     return render(request, 'file_create_form.html', {'form': form})


class AddEntities(PermissionRequiredMixin, CreateView):
    permission_required = 'system.add_entities'
    form_class = EntitiesForm
    template_name = 'entities_create_form.html'
    success_url = reverse_lazy('entities-form')
    logger.info("New category added")


#TODO:remake entities_form function in class method
def entities_form(request):
    """
    This function handles the creation of entities form. It takes in a request object and returns a rendered HTML page with the form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML page with the form.

    Raises:
        None
    """
    # if request.method == 'POST':
    #     form=EntitiesForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         try:
    #             form.save()
    #             return HttpResponseRedirect("/form")
    #             #return redirect('form-test')
    #         except:
    #             form.add_error(None, 'Add data error')
    # else:
    #     form=EntitiesForm()
    # return render(request, 'entities_create_form.html', {'form': form})



#Form for add new documents
# def document_form(request):
#     if request.method == 'POST':
#         form=DocumentsAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return HttpResponseRedirect("/add-document")
#                 #return redirect('form-test')
#             except:
#                 form.add_error(None, 'Add data error')
#     else:
#         form=DocumentsAddForm()
#     return render(request, 'document_create_form.html', {'form': form})


#TODO:remake files_form function in class method
def files_form(request):
    """
    This function handles the creation of a new file through a form submission. It takes in a request object and returns a rendered HTML template with the form.

    Args:
        request (HttpRequest): The HTTP request object containing the form data.

    Returns:
        HttpResponse: A rendered HTML template with the form.
    """

    if request.method == 'POST':
        form=FilesAddForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect("/add-file")
                #return redirect('form-test')
            except:
                form.add_error(None, 'Add data error')
    else:
        form=FilesAddForm()
    return render(request, 'file_create_form.html', {'form': form})


#Users registration
# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     group_required = [u'Нет']
#     default_group, created = Group.objects.get_or_create(name='Нет')
#     User.groups.default(default_group)
#     group = Group.objects.get(name='Нет')
#     user = super().save(commit=False)
#     user.groups.add(group)
#     template_name = 'register.html'
#     success_url = reverse_lazy("login")
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #c_def = self.get_user_context(title='Registration')
#         return dict(list(context.items()))

#TODO: remake function in class method
def UserRegister(request):
    """
    Registers a new user with the provided request data.

    Args:
        request (HttpRequest): The HTTP request object containing user registration data.

    Returns:
        HttpResponseRedirect: A redirect to the login page upon successful user registration.

    """
    logger.info("New account registration")
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Нет доступа')
            user.groups.add(group)
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})


# Авторизация пользователей
class LoginUser(LoginView):
    """
            A class-based view for user login.

            :param form_class: The form class to use for user authentication.
            :type form_class: django.forms.Form
            :param template_name: The name of the template to use for rendering the login page.
            :type template_name: str
            """
    logger.info("User login ")
    form_class=AuthenticationForm
    template_name = 'login.html'
    #success_url = reverse_lazy("category-list")
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Returns a dictionary of context data for the current view.

        :param object_list: A list of objects to be used in the view.
        :type object_list: list, optional
        :param kwargs: Additional keyword arguments to be passed to the parent method.
        :type kwargs: dict
        :return: A dictionary of context data for the current view.
        :rtype: dict
        """

        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.

        :return: A string representing the URL to redirect to.
        :rtype: str
        """
        return reverse_lazy('category-list')

def logout_user(request):
    """
    Logs out the user associated with the given request and redirects to the category list page.

    Args:
        request (HttpRequest): The request object representing the current request.

    Returns:
        HttpResponseRedirect: A redirect response to the category list page.
    """
    logout(request)
    return redirect('category-list')


class ViewFiles(ListView):
    """
        A class-based view that displays a list of files.

        Args:
            ListView: A Django generic view that displays a list of objects.

        Attributes:
            model (Model): The model that the view will use to retrieve the list of files.
            template_name (str): The name of the template that will be used to render the view.

        Returns:
            A rendered HTML template displaying a list of files.
    """
    model = Files
    template_name = 'files_view.html'


class ViewDocument(ListView):

    model = Documents
    template_name = 'docs_views.html'

class FileUpdate(UpdateView):
    """
    A class-based view for updating an existing file object.

    Args:
        UpdateView: A Django generic view for updating an object.

    Attributes:
        model (Model): The model class that the view will be working with.
        template_name (str): The name of the template to be rendered.
        fields (set): The fields that will be displayed in the form.

    Returns:
        A rendered HTML template with a form for updating an existing file object.
    """
    logger.info("File Update ")
    model = Files
    template_name = 'update_files.html'
    fields = {'file_name', 'file', 'file_version'}
    success_url = reverse_lazy("category-list")



class FilesToCategories(CreateView):
    """
    A class-based view that handles the creation of a new relation between a file and a category.

    Attributes:
        form_class (RelationFileForm): The form class used for creating a new relation.
        template_name (str): The name of the template used for rendering the view.
        success_url (reverse_lazy): The URL to redirect to upon successful creation of a new relation.

    Methods:
        get_context_data: Adds extra context data to the template.
    """
    #logger.info("Файл привязан к категории ")
    form_class = RelationFileForm
    template_name = 'file_to_category.html'
    success_url = reverse_lazy('file-form')


class DocumentsToFiles(CreateView):
    """
    A class-based view that handles the creation of a new relation between a file and a category.

    Attributes:
        form_class (RelationFileForm): The form class used for creating a new relation.
        template_name (str): The name of the template used for rendering the view.
        success_url (reverse_lazy): The URL to redirect to upon successful creation of a new relation.

    Methods:
        get_context_data: Adds extra context data to the template.
    """
    #logger.info("Документ привязан к файлу ")
    form_class = RelationDocumetnForm
    template_name = 'document_to_file.html'
    success_url = reverse_lazy('doc-files')


class SearchFiles(ListView):

    model = Files
    template_name = 'search_file_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        object_list = Files.objects.filter(
            Q(file_name__icontains=query)
        )

        return object_list


class SearchDocs(ListView):

    model = Documents
    template_name = 'search_docs_result.html'

    def get_queryset(self):
        query = self.request.GET.get('w')

        object_list = Documents.objects.filter(
            Q(doc_name__icontains=query)
        )


        return object_list

class Search(ListView):

    template_name = 'searching.html'

    def get_queryset(self):
        result_list = []
        #matches = Files.objects.all() | Documents.objects.all()
        #print('Вот оно:')
        #print(matches)
        q = self.request.GET.get('z')
        print('Вот оно:')
        docs_list = Documents.objects.filter(
            Q(doc_name__icontains=q)
        )
        print(docs_list)
        files_list = Files.objects.filter(
            Q(file_name__icontains=q)
            )
        print((files_list))

        
        #result_list = list(chain(files_list, docs_list))

        #print(result_list)


        return result_list

# class SearchView(View):
#
#     template_name = 'searching.html'
#     def get(self, request, *args, **kwargs):
#         context = {}
#
#         q = request.GET.get('z')
#         if q:
#             query_sets = []  # Total QuerySet
#
#             # Searching for all models
#             query_sets.append(Files.objects.search(query=q))
#             query_sets.append(Documents.objects.search(query=q))
#
#
#             # and combine results
#             final_set = list(chain(*query_sets))
#             object_list = Documents.objects.filter(
#                 Q(content__icontains=final_set)
#             )
#             #final_set.sort(key=lambda x: x.pub_date, reverse=True)  # Sorting
#             print(final_set)
#
#
#
#
#
#         return object_list

        #return render(request=request, template_name=self.template_name, context=context)


class DeleteCategory(DeleteView):
    #logger.info("Категория удалена ")
    model = Entities
    template_name = 'cat_delete.html'


@login_required
@permission_required("system.delete_entities", raise_exception=True)
def delete_cat(request, new_id):
    """
    Deletes a category entity with the given ID.

    Args:
        request (HttpRequest): The HTTP request object.
        new_id (int): The ID of the cat entity to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the homepage after deleting the cat entity.

    Raises:
        Http404: If the cat entity with the given ID does not exist.
        PermissionDenied: If the user does not have permission to delete entities.
    """
    logger.info("Категория удалена ")
    new_to_delete = get_object_or_404(Entities, id=new_id)

    if request.method == 'POST':
        form = DeleteCatForm(request.POST, instance=new_to_delete)

        if not request.user.has_perm('system.delete_entities'):
            raise PermissionDenied
        else:
            new_to_delete.delete()
            return HttpResponseRedirect("/") # wherever to go after deleting

    else:
        form = DeleteCatForm(instance=new_to_delete)

    template_vars = {'form': form}
    return render(request, 'cat_delete.html', template_vars)


def change_password(request):
    #logger.info("Пароль изменен ")
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
        else:
            messages.error(request, 'Please correct the error below')
            return HttpResponseRedirect("/password-change")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'password_change_form.html', {'form': form})
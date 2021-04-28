from django.shortcuts import render
from django.views import generic
from .models import Book, Author, Genre, BookInstance, Language

# Create your views here.
def index(request):
    """
    Función vista para la pagina de inicio.
    """
    # Contadores de books y copias de books
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Obtenemos copias disponibles
    num_instances_available = BookInstance.objects.filter(
        status__exact='a' 
    ).count()
    num_authors = Author.objects.count() # .all() está implicito
    num_genres = Genre.objects.count()
    num_titles_search = Book.objects.filter(
        title__icontains='harry'
    ).count() # consultar porque no es case-sensitive si no uso la i
    
    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    # Renderizando plantilla index.html con datos obtenidos
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors' : num_authors,
            'num_genres': num_genres,
            'num_titles_search': num_titles_search,
            'num_visits': num_visits
        }
    )
    
class BookListView(generic.ListView):
    """
    Clase usada para listar todos los books
    Recordar uso de generic.ListView
    """
    model = Book
    context_object_name = 'book_list' # nombre de la variable a pasar al template
    queryset = Book.objects.all() 
    template_name = 'books/list.html'
    paginate_by = 5 # Paginar para solo cargar los 5 primeros records
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail-view.html'
    context_object_name = 'book'
    
class AuthorListView(generic.ListView):
    """
    Clase para listar todos los autores
    """
    model = Author
    context_object_name = 'authors_list'
    queryset = Author.objects.all()
    paginate_by = 5
    template_name = 'authors/list.html'
    
class AuthorDetailView(generic.DetailView):
    """
    Clase para mostrar detalles de cada autor
    Extiende de clase generica --> No reinventar rueda
    """
    
    model = Author
    context_object_name = 'author'
    template_name = 'authors/detail-view.html'

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based for listing books on loan to current
    user. LoginRequiredMixing allows authentication
    """
    model = BookInstance
    template_name = 'user/borrowed_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(
            status__exact='o'
        ).order_by('due_back')
        
class AllLoanedBooksListView(LoginRequiredMixin,
                             PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based for listing all loaned books per person
    Required permission as a Librarian
    This will show 403 error for unathorized user
    """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by = 5
    template_name = 'books/all-loaned.html'
    
    def get_queryset(self):
        return BookInstance.objects.filter(
            status__exact='o'
        ).order_by('due_back')
        
# class AllLoanedBooksListView(LoginRequiredMixin, generic.ListView):
#     """
#     Generic class-based for listing all loaned books per person
#     The permissions wil be controlled in the template
#     """
#     model = BookInstance
#     paginate_by = 5
#     template_name = 'books/all-loaned.html'
    
#     def get_queryset(self):
#         return BookInstance.objects.filter(
#             status__exact='o'
#         ).order_by('due_back')
        
"""
Que es mejor? Control de perms en View o en Template?
"""
"""
Trabajar con formularios
"""
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm, RenewBookModelForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    Using ModelForm
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(
            initial={'due_back': proposed_due_back,})

    return render(
        request, 'catalog/book_renew_librarian.html',
        {'form': form, 'bookinst':book_inst}
        )
    
# @permission_required('catalog.can_mark_returned')
# def renew_book_librarian(request, pk):
#     """
#     View function for renewing a specific BookInstance by librarian
#     Using form
#     """
#     book_inst=get_object_or_404(BookInstance, pk = pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_inst.due_back = form.cleaned_data['renewal_date']
#             book_inst.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('all-borrowed') )

#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(
#             initial={'renewal_date': proposed_renewal_date,})

#     return render(
#         request, 'catalog/book_renew_librarian.html',
#         {'form': form, 'bookinst':book_inst}
#         )

"""
Generic Editing Views
"""
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

"""Author"""
class AuthorCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/10/2018',}
    
    
class AuthorUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    
    
class AuthorDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_mark_returned'  
    model = Author
    success_url = reverse_lazy('authors')
    
"""
Falta agregar en la lista de autores links a: Crear, editar, eliminar
"""
"""Book"""
class BookCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'
    
    
class BookUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'
    
    
class BookDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_mark_returned'  
    model = Book
    success_url = reverse_lazy('books')
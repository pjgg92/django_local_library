from django.contrib import admin
from .models import (
    Genre, Book, Author, BookInstance, Language
    )

# Register your models here.

# Registramos admin clases a partir del decorador

class BookInline(admin.TabularInline):
    model = Book
    extra = 0 # Evita que aparezcan registros para rellenar
    fields = ['title', 'isbn','genre']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Clase que permite modificar el aspecto de la seccion
    referente al modelo Author dentro del panel de
    administrador
    """
    list_display = ['first_name', 'last_name']
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    """Nota: Puedes también usar el atributo exclude para declarar una lista
    de atributos que se excluirán del formulario (todos los demás atributos
    en el modelo se desplegarán)."""

class BookInstanceInline(admin.TabularInline):
    """
    Clase que nos permite crear informacion encadenada
    de forma tabular con la info de los BookInstances
    que tenemos en la bbdd.
    Esta clase siempre debe aparecer antes de la clase
    que la implementa
    """
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Clase que permite modificar el aspecto de la seccion
    referente al modelo Book dentro del panel de
    administrador
    """
    list_display = ['title', 'author', 'display_genre']
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """
    Clase que permite modificar el aspecto de la seccion
    referente al modelo BookInstance dentro del panel de
    administrador
    """
    list_display = ["book", "status",'due_back', 'borrower', 'id']
    list_filter = ['status', 'due_back']
    
    fieldsets = (
        ('Info',{
            'fields': ('book', 'id')
        }),
        ('Availability',{
            'fields': ('status', 'due_back','borrower')
        }),
    )



admin.site.register(Language)
admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
# registrando nueva clase AuthorAdmin
# admin.site.register(AuthorAdmin)

"""
Falta Hacer reto

"""
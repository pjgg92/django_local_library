from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

import uuid
"""
fuente resolucion:
https://github.com/mdn/django-locallibrary-tutorial
"""
class Genre(models.Model):
    """
    Modelo que representa el género literario.
    Ejemplos: ciencia ficcion, poesia, drama, terror
    """
    name = models.CharField(
        max_length=200,
        help_text="Ingrese el género del libro (Ciencia ficción, poesía, etc)"
    )
    
    def __str__(self):
        """
        Cadena que representa la instancia del modelo.
        Por ejemplo, en el sitio Admin.
        Tiene que describir la instancia
        """
        return self.name

class Book(models.Model):
    """
    Modelo que representa un libro.
    """
    #campos
    title = models.CharField(
        max_length=200,
        help_text="Ingrese el titulo del libro"
    )
    """
    Ojo con author que tiene una relacion con el modelo Author
    1 Book tiene 1 Author (El UML pone 1 a muchos)
    1 Author tiene 0..* Books
    """
    author = models.ForeignKey(
        "Author",
        on_delete=models.SET_NULL,
        null=True
    )
    summary = models.TextField(
        max_length="10000",
        help_text="Introduzca un resumen del libro"
    )
    # imprint = models.CharField(max_length=200)
    isbn = models.CharField("ISBN",max_length=13)
    genre = models.ManyToManyField(
        Genre,
        help_text="Seleccione un género de la lista"
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.SET_NULL,
        null=True
    )
    
    #metodos
    def __str__(self):
        """
        Se devuelve el titulo  + iso code como representacion
        del objeto Book y su idioma
        """
        return f'{self.title}[{self.language.iso_code}]'
    
    def get_absolute_url(self):
        """
        Devuelve una URL para cada instancia de Book
        """
        return reverse("book-detail", args=[str(self.id)])
    
    def display_genre(self):
        """
        Devuelve una concatenacion de los generos del libro
        """
        return(
            ', '.join([genre.name for genre in self.genre.all()[:3]])
        )
    """
    short_description establece la descripcion corta a mostrar
    como cabecera del campo de la tabla de la bbdd
    """
    display_genre.short_description = 'Genres'
    
class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro
    """
    #Campos
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para el libro en toda la biblioteca"
    )
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='m',
        blank=True,
        help_text="Disponibilidad del libro"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True
    )
    """
    1 BookInstance can only have 0-1 borrower,
    1 Borrower can have 0-* BookInstance
    """
    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
        
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    class Meta():
        """
        Ordenando las copias de libro
        segun fecha prevista de recepcion
        """
        ordering = ["status","due_back"]
        permissions = (("can_mark_returned","Set book as returned"),)
    
    def __str__(self):
        """
        Representa el objeto de copia de libro
        """
        return(
            f'{self.book} | {self.id}'
        )
        
class Author(models.Model):
    """
    Modelo que representa un autor (author)
    """
    #campos
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    date_of_death = models.DateField(
        verbose_name='died',
        null=True,
        blank=True
    )
    
    #Metodos
    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular
        de un autor.
        """
        return reverse(
            "author-detail",
            args=[str(self.id)]
        )
    
    def __str__(self):
        return (
            f'{self.last_name}, {self.first_name}'
        )
        
class Language(models.Model):
    """
    Modelo que representa un idioma
    """
    # Campos
    iso_code = models.CharField(
        max_length=2,
        unique=True,
        help_text="Introduza codigo de 2 letras del idioma (ISO 639)"
    )
    
    language = models.CharField(
        max_length=30,
        help_text="Introduzca el nombre del idioma"
    )
    
    # Metodos
    def __str__(self):
        return self.language
    

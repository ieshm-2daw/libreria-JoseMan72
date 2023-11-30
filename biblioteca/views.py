from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Libro

# Create your views here.

# lista, detalle y modificar
'''
class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/libro_list.html'
'''
# librolistview pero que solo muestre los libros disponibles
class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/libro_list.html'

    #queryset = Libro.objects.filter(disponibilidad='D')
    ''' Otra forma sobrescribiendo el metodo get_queryset
    def get_queryset(self): #sobreescribimos el metodo get_queryset, que sirve para filtrar los libros disponibles pasandole el parametro 'D'
        return Libro.objects.filter(disponibilidad='D')
    '''

    #filtrar los libros disponibles y no disponibles
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad='D')
        context['libros_prestados'] = Libro.objects.filter(disponibilidad='P')

        return context

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'biblioteca/libro_detail.html'

class LibroUpdateView(UpdateView):
    model = Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion', 'genero', 'isbn', 'resumen', 'portada', 'disponibilidad']
    template_name = 'biblioteca/libro_edit.html'
    success_url = reverse_lazy('libro_list')

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'biblioteca/libro_delete.html'
    success_url = reverse_lazy('libro_list')

class LibroCreateView(CreateView):
    model = Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion', 'genero', 'isbn', 'resumen', 'portada', 'disponibilidad']
    template_name = 'biblioteca/libro_create.html'
    success_url = reverse_lazy('libro_list')
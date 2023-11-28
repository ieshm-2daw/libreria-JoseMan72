from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Libro

# Create your views here.

# lista, detalle y modificar

class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/libro_list.html'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'biblioteca/libro_detail.html'

class LibroUpdateView(UpdateView):
    model = Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion', 'genero', 'isbn', 'resumen', 'portada', 'disponibilidad']
    template_name = 'biblioteca/libro_edit.html'

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'biblioteca/libro_delete.html'
    success_url = reverse_lazy('lista_libros')

class LibroCreateView(CreateView):
    model = Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion', 'genero', 'isbn', 'resumen', 'portada', 'disponibilidad']
    template_name = 'biblioteca/libro_create.html'
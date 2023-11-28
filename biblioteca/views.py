from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from .models import Libro

# Create your views here.

# lista, detalle y modificar

class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libro_detail.html'

class LibroUpdateView(UpdateView):
    model = Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion', 'genero', 'isbn', 'resumen', 'portada', 'disponibilidad']
    template_name = 'libro_edit.html'
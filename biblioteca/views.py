import datetime
from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .models import Libro, Prestamo

# Create your views here.

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
        context['libros_en_proceso'] = Libro.objects.filter(disponibilidad='E')

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

''' Este funciona pero se puede hacer sin kwargs
class LibroLoanView(View):
    def get(self, request, *args, **kwargs):
        libro = Libro.objects.get(pk=kwargs['pk']) #obtenemos el libro que queremos prestar
        return render(request, 'biblioteca/libro_loan.html', {'libro': libro})
    
    def post(self, request, *args, **kwargs):
        libro = Libro.objects.get(pk=kwargs['pk'])
        libro.disponibilidad = 'P' #Cambiamos la disponibilidad del libro a prestado
        libro.save()
        return redirect('libro_list') #Redirigimos a la lista de libros
'''
class LibroLoanView(View):
    def get(self, request, pk):
        libro = Libro.objects.get(id=pk) #dentro del get, pk es el parametro que le pasamos en la url e id es el campo de la base de datos
        return render(request, 'biblioteca/libro_loan.html', {'libro': libro})
    
    def post(self, request, pk):
        libro = Libro.objects.get(id=pk) #dentro del get, pk es el parametro que le pasamos en la url e id es el campo de la base de datos
        libro.disponibilidad = 'P' #Cambiamos la disponibilidad del libro a prestado
        libro.save()

        #Se crea un nuevo prestamo
        prestamo = Prestamo()
        prestamo.libro = libro
        prestamo.fecha_prestamo = datetime.datetime.now()
        prestamo.usuario = request.user
        prestamo.estado = 'P'
        prestamo.save()
        return redirect('libro_list') #Redirigimos a la lista de libros

''' Lo mismo pero con funciones
def libro_loan(request, pk):
    if request.method == 'GET':
        libro = Libro.objects.get(id=pk)
        return render(request, 'biblioteca/libro_loan.html', {'libro': libro})
    elif request.method == 'POST':
        libro = Libro.objects.get(id=pk)
        libro.disponibilidad = 'P'
        libro.save()
        
        #Se crea un nuevo prestamo
        prestamo = Prestamo()
        prestamo.libro = libro
        prestamo.fecha_prestamo = datetime.now()
        prestamo.usuario = request.user
        prestamo.estado = 'P'
        prestamo.save()
        return redirect('libro_list')
'''
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
        #prestamo.fecha_prestamo = fecha_prestamo + timedelta(days=15)
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

class PrestamosListView(ListView): #Lista de prestamos el cual no es necesario
    model = Prestamo
    template_name = 'biblioteca/prestamo_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['prestados'] = Prestamo.objects.filter(estado='P')
        context['devueltos'] = Prestamo.objects.filter(estado='D')
        return context

class MisLibroListView(ListView):
    model = Prestamo
    template_name = 'biblioteca/mislibros_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['prestados'] = Prestamo.objects.filter(estado='P', usuario=self.request.user)
        context['devueltos'] = Prestamo.objects.filter(estado='D', usuario=self.request.user)
        return context

class ReturnBookView(View):
    def get(self, request, pk):
        prestamo = Prestamo.objects.get(id=pk)
        return render(request, 'biblioteca/return_book.html', {'prestamo': prestamo})
    
    def post(self, request, pk):
        prestamo = Prestamo.objects.get(id=pk)
        prestamo.estado = 'D'
        prestamo.fecha_devolucion = datetime.datetime.now()
        prestamo.save()

        libro = prestamo.libro
        libro.disponibilidad = 'D'
        libro.save()
        return redirect('mislibros_list')

#Libros mas prestados
class MoreLoansListView(View):
    def get(self, request):
        libros = Libro.objects.all()
        lista_mas_prestados = []
        for libro in libros:
            prestamos = Prestamo.objects.filter(libro=libro) #Obtenemos los prestamos de ese libro
            #Obtenemos los usuarios a los que se les ha prestado ese libro, dentro de prestamos tenemos el campo usuario que es el que nos interesa
            usuarios = prestamos.values_list('usuario__username', flat=True).distinct #flat=True para que nos devuelva una lista de strings y no una lista de tuplas
            #Añadimos a la lista el libro, el numero de prestamos y los usuarios
            lista_mas_prestados.append([libro, len(prestamos), usuarios])
        lista_mas_prestados.sort(key=lambda x: x[1], reverse=True) #Ordenamos la lista de mayor a menor por el numero de prestamos
        return render(request, 'biblioteca/moreloans_list.html', {'lista_mas_prestados': lista_mas_prestados})

'''
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        libros = Libro.objects.all()
        libros_mas_prestados = []
        for libro in libros:
            prestamos = Prestamo.objects.filter(libro=libro)
            libros_mas_prestados.append([libro, len(prestamos)])
        libros_mas_prestados.sort(key=lambda x: x[1], reverse=True)
        context['libros_mas_prestados'] = libros_mas_prestados
        return context'''
import datetime
from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .models import Libro, Prestamo
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/libro_list.html'
    context_object_name = 'libros_genero'

    #librolistview pero que solo muestre los libros disponibles
    #   queryset = Libro.objects.filter(disponibilidad='D')
    ''' Otra forma sobrescribiendo el metodo get_queryset
    def get_queryset(self): #sobreescribimos el metodo get_queryset, que sirve para filtrar los libros disponibles pasandole el parametro 'D'
        return Libro.objects.filter(disponibilidad='D')
    '''

    #filtrar los libros disponibles, no disponibles y en proceso
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        genero = self.request.GET.get('genero', '') #Para el filtro de genero
        context['genero'] = genero
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad='D')
        context['libros_prestados'] = Libro.objects.filter(disponibilidad='P')
        context['libros_en_proceso'] = Libro.objects.filter(disponibilidad='E')
        return context

    def get_queryset(self):
        queryset = Libro.objects.all()
        genero = self.request.GET.get('genero')

        if genero:
            queryset = queryset.filter(genero=genero)
        return queryset

class LibroDetailView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = 'biblioteca/libro_detail.html'

class LibroUpdateView(LoginRequiredMixin, UpdateView):
    model = Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion', 'genero', 'isbn', 'resumen', 'portada', 'disponibilidad']
    template_name = 'biblioteca/libro_edit.html'
    success_url = reverse_lazy('libro_list')

class LibroDeleteView(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = 'biblioteca/libro_delete.html'
    success_url = reverse_lazy('libro_list')

class LibroCreateView(LoginRequiredMixin, CreateView):
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
class LibroLoanView(LoginRequiredMixin, View):
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

class PrestamosListView(LoginRequiredMixin, ListView): #Lista de prestamos el cual no es necesario
    model = Prestamo
    template_name = 'biblioteca/prestamo_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['prestados'] = Prestamo.objects.filter(estado='P')
        context['devueltos'] = Prestamo.objects.filter(estado='D')
        return context

class MisLibroListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'biblioteca/mislibros_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['prestados'] = Prestamo.objects.filter(estado='P', usuario=self.request.user)
        context['devueltos'] = Prestamo.objects.filter(estado='D', usuario=self.request.user)
        return context

class ReturnBookView(LoginRequiredMixin, View):
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
class MoreLoansListView(LoginRequiredMixin, View):
    def get(self, request):
        libros = Libro.objects.all()
        lista_mas_prestados = []
        for libro in libros:
            prestamos = Prestamo.objects.filter(libro=libro) #Obtenemos los prestamos de ese libro
            #Obtenemos los usuarios a los que se les ha prestado ese libro, dentro de prestamos tenemos el campo usuario que es el que nos interesa
            usuarios = []
            for prestamo in prestamos:
                if prestamo.usuario.username not in usuarios:
                    usuarios.append(prestamo.usuario.username)
            
            #Añadimos el numero de prestado de ese libro a ese usuario, de forma que cambia de 'joseman7' a 'joseman7 (2)'
            for usuario in usuarios:
                contador = 0
                for prestamo in prestamos:
                    if prestamo.usuario.username == usuario:
                        contador += 1
                if contador > 1:
                    usuarios[usuarios.index(usuario)] = usuario + ' (' + str(contador) + ')'
            
            #Añadimos a la lista el libro, el numero de prestamos y los usuarios
            lista_mas_prestados.append([libro, len(prestamos), usuarios])
        lista_mas_prestados.sort(key=lambda x: x[1], reverse=True) #Ordenamos la lista de mayor a menor por el numero de prestamos
        return render(request, 'biblioteca/moreloans_list.html', {'lista_mas_prestados': lista_mas_prestados})

''' Panel
N de libros prestados: 
N de libros disponibles:
Libros no devueltos: ( se han pasado de la fecha)
Libros proximos a devolver: (se acerca la fecha de devolucion, ultima semana)
Top libros
'''

class PanelBibliotecarioView(LoginRequiredMixin, View):
    def get(self, request):
        libros = Libro.objects.all()
        lista_prestados = 0             #Numero de libros prestados
        lista_disponibles = 0           #Numero de libros disponibles
        lista_no_devueltos = Prestamo.objects.filter(estado='P', fecha_devolucion__lt=datetime.datetime.now())       #Libros que se han pasado de la fecha de devolucion
        lista_proximos_devolver = Prestamo.objects.filter(estado='P',fecha_devolucion__gte=datetime.datetime.now(), fecha_devolucion__lte=(datetime.datetime.now() + datetime.timedelta(days=7)))    #Libros que se acerca la fecha de devolucion (ultima semana)

        for libro in libros:
            if libro.disponibilidad == 'P':
                lista_prestados += 1
            elif libro.disponibilidad == 'D':
                lista_disponibles += 1
        
        return render(request, 'biblioteca/panel.html', {'lista_prestados': lista_prestados, 'lista_disponibles': lista_disponibles, 'lista_no_devueltos': lista_no_devueltos, 'lista_proximos_devolver': lista_proximos_devolver})

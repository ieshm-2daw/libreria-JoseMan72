from django.db import models

# Create your models here.
'''
1. Usuario: Esta clase debe extender AbstractUser de Django e incluir los campos adicionales como dni, dirección, y teléfono.
2. Libro: Un modelo que represente los libros de la biblioteca. Debe tener campos como título, autor(es), editorial, 
    fecha de publicación, género, ISBN, resumen, disponibilidad (posibles valores: disponible, prestado, en proceso de préstamo), portada, etc.
3. Autor: Modelo que contiene a los autores con los campos: nombre biografía y foto.
4. Editorial: con los campos nombre, dirección y sitio web.
5. Préstamo: Un modelo para registrar los préstamos de libros a los usuarios. Debe contener campos para el libro prestado, 
    la fecha de préstamo, la fecha de devolución, el usuario que lo prestó y el estado del préstamo (prestado, devuelto).
'''
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=9, unique=True)
    direccion = models.TextField()
    telefono = models.IntegerField()

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autores = models.ManyToManyField('Autor')
    editorial = models.ForeignKey('Editorial', on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    
    #genero tendrá opciones de selección, por ejemplo: novela, ensayo, cuento, etc.
    GENEROS = (
        ('N', 'Novela'),
        ('C', 'Cuento'),
        ('P', 'Poesía'),
        ('T', 'Teatro'),
        ('O', 'Otros'),
    )
    genero = models.CharField(max_length=1, choices=GENEROS)
    isbn = models.IntegerField(max_length=13, unique=True)
    resumen = models.TextField()

    DISPONIBILIDAD = (
        ('D', 'Disponible'),
        ('P', 'Prestado'),
    )
    disponibilidad = models.CharField(max_length=1, choices=DISPONIBILIDAD)
    #portada = models.ImageField() #Neceista Pillow

class Autor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    biografia = models.TextField()
    #foto = models.ImageField() #Necesita Pillow

class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    sitio_web = models.URLField() #default='https://es.wikipedia.org/wiki/'

class Prestamo(models.Model):
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    ESTADO = (
        ('P', 'Prestado'),
        ('D', 'Devuelto'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO)
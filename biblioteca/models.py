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
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    #foto = models.ImageField() #Hace falta instalar Pillow
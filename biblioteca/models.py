from django.db import models
from django.core.validators import MaxValueValidator

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

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    #foto = models.ImageField(upload_to='autores/', null=True, blank=True) #Necesita Pillow

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(max_length=200)
    sitio_web = models.URLField()

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autores = models.ManyToManyField(Autor)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    fecha_publicacion = models.DateField()
    
    #genero tendrá opciones de selección, por ejemplo: novela, cuento, poesía, teatro, otros.
    GENEROS = (
        ('N', 'Novela'),
        ('C', 'Cuento'),
        ('P', 'Poesía'),
        ('T', 'Teatro'),
        ('O', 'Otros'),
    )
    genero = models.CharField(max_length=1, choices=GENEROS)
    isbn = models.IntegerField(max_length=13)
    resumen = models.TextField()
    #portada = models.ImageField(upload_to='portadas/', null=True, blank=True) #Necesita Pillow

    DISPONIBILIDAD = (
        ('D', 'Disponible'),
        ('P', 'Prestado'),
        ('E', 'En proceso de prestamo'),
    )
    disponibilidad = models.CharField(max_length=1, choices=DISPONIBILIDAD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ESTADO = (
        ('P', 'Prestado'),
        ('D', 'Devuelto'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO, default='P')

    def __str__(self):
        return f"Prestamo de {self.libro} a {self.usuario}"
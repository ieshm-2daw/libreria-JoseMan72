from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Autor, Editorial, Libro

# Register your models here.
admin.site.register(Usuario, UserAdmin)
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Libro)
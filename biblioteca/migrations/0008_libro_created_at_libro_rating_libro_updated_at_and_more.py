# Generated by Django 4.2.7 on 2023-11-24 11:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0007_alter_libro_disponibilidad_alter_libro_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='libro',
            name='rating',
            field=models.PositiveIntegerField(default=' ', validators=[django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='libro',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='autor',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='editorial',
            name='direccion',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='editorial',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='libro',
            name='disponibilidad',
            field=models.CharField(choices=[('D', 'Disponible'), ('P', 'Prestado'), ('E', 'En proceso de prestamo')], max_length=1),
        ),
        migrations.AlterField(
            model_name='libro',
            name='isbn',
            field=models.IntegerField(max_length=13),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='estado',
            field=models.CharField(choices=[('P', 'Prestado'), ('D', 'Devuelto')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha_devolucion',
            field=models.DateField(blank=True, null=True),
        ),
    ]

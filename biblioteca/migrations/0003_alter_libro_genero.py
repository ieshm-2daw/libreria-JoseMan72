# Generated by Django 4.2.7 on 2024-01-09 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0002_alter_usuario_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='genero',
            field=models.CharField(choices=[('Novela', 'Novela'), ('Cuento', 'Cuento'), ('Poesia', 'Poesia'), ('Teatro', 'Teatro'), ('Otros', 'Otros')], max_length=10),
        ),
    ]

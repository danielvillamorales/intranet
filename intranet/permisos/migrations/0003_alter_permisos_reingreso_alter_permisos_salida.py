# Generated by Django 4.0.3 on 2022-05-10 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0002_alter_permisos_fechafinal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permisos',
            name='reingreso',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='permisos',
            name='salida',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.1.7 on 2023-10-23 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cajas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cajas',
            options={'permissions': [('ver_cajas', 'ver_cajas'), ('ver_todas_las_cajas', 'ver_todas_las_cajas')]},
        ),
    ]
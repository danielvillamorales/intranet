# Generated by Django 4.2.6 on 2024-02-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0009_usuariohorarios_horariosporteria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horariosporteria',
            name='totalhoras',
            field=models.FloatField(),
        ),
    ]
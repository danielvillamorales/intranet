# Generated by Django 4.0.3 on 2022-05-10 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permisos',
            name='fechaFinal',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='permisos',
            name='fechaInicial',
            field=models.DateTimeField(null=True),
        ),
    ]

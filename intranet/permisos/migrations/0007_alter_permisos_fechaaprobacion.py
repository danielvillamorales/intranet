# Generated by Django 4.1.3 on 2023-03-01 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("permisos", "0006_permisos_fechacreacion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permisos",
            name="fechaaprobacion",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.1.3 on 2023-03-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("directorio", "0002_convenios"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promociones",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=250)),
                ("fecha_inicial", models.DateField()),
                ("fecha_final", models.DateField()),
                ("descripcion", models.CharField(max_length=10000)),
                ("banner", models.ImageField(upload_to="imagenes/")),
            ],
            options={"db_table": "promociones",},
        ),
    ]

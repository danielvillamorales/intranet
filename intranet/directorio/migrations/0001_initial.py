# Generated by Django 4.1.3 on 2023-03-08 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cargos",
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
                ("codigo", models.IntegerField()),
                ("descripcion", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Ciudades",
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
                ("codigo", models.IntegerField()),
                ("descripcion", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Sedes",
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
                ("codigo", models.CharField(max_length=5)),
                ("descripcion", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Directorio",
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
                ("usuario", models.CharField(max_length=255)),
                ("extension", models.CharField(blank=True, max_length=30, null=True)),
                ("telefono", models.CharField(blank=True, max_length=30, null=True)),
                ("email", models.CharField(blank=True, max_length=255, null=True)),
                ("direccion", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "cargo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directorio.cargos",
                    ),
                ),
                (
                    "ciudad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directorio.ciudades",
                    ),
                ),
                (
                    "sede",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directorio.sedes",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dir_almacenes",
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
                ("almacen", models.CharField(max_length=200)),
                ("direccion", models.CharField(max_length=200)),
                ("horario", models.CharField(max_length=200)),
                ("telefono", models.CharField(max_length=200)),
                ("correo", models.CharField(max_length=200)),
                ("contacto", models.CharField(max_length=200)),
                (
                    "ciudad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directorio.ciudades",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Did",
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
                ("indicativo", models.CharField(max_length=5)),
                ("numero", models.CharField(max_length=50)),
                (
                    "ciudad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directorio.ciudades",
                    ),
                ),
            ],
        ),
    ]

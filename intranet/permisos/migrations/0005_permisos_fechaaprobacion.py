# Generated by Django 4.0.5 on 2022-06-10 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0004_alter_permisos_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='permisos',
            name='fechaaprobacion',
            field=models.DateTimeField(null=True),
        ),
    ]
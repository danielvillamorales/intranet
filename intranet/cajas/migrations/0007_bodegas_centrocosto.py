# Generated by Django 4.2.6 on 2023-11-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajas', '0006_alter_cajas_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodegas',
            name='centrocosto',
            field=models.CharField(default='13102', max_length=15),
        ),
    ]
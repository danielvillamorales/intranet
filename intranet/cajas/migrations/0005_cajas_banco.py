# Generated by Django 4.1.7 on 2023-10-24 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajas', '0004_cajas_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='cajas',
            name='banco',
            field=models.CharField(default='BANCOLOMBIA', max_length=50),
        ),
    ]

from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Bodegas(models.Model):
    codigo = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'


class UsuarioBodega(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usuariobod')
    bodega = models.ForeignKey(Bodegas, on_delete=models.PROTECT, related_name='bodega')


    def __str__(self):
        return f'{self.usuario.first_name}  {self.usuario.last_name} - {self.bodega}'
    

class Cajas(models.Model):
    bodega = models.ForeignKey(Bodegas, on_delete=models.PROTECT)
    fecha = models.DateField()
    valor = models.IntegerField()
    banco = models.CharField(max_length=50, default='BANCOLOMBIA')
    observacion = models.CharField(max_length=300, default=f'consignacion dia {date.today()}')
    imagen = models.ImageField(upload_to='cajas')

    def __str__(self):
        return f'{self.bodega} - {self.fecha}'
    
    class Meta:
        permissions = [('ver_cajas','ver_cajas'),('ver_todas_las_cajas','ver_todas_las_cajas')]
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tipodepermiso(models.Model):
    descripcion = models.CharField(null=False,blank=False,max_length=255)
    es_beneficio = models.IntegerField(null=False, blank=False,default=0,help_text=' 1:es tipo beneficio , 0:no lo es ')
    
    def __str__(self) :
        return self.descripcion


class Beneficios(models.Model):
    nombre = models.CharField(blank=False,null=False,unique=True,max_length=100,help_text='nombre del beneficio a crear')
    detalle= models.CharField(blank=False,null=False,max_length=500,help_text='detalles de que es el benefecion ejemplo tiempo para ti es un dia al año libre')
    condiciones= models.CharField(blank=False,null=False,max_length=500,help_text='es la descripcion de que tiene que cumplir el empleado para poder aplicar')
    catidadDeSolicitudes = models.IntegerField(help_text='numero de solicitudes que puede hacer la persona de este beneficio')
    estado = models.IntegerField(default=1, null=False,help_text='estado 1:activo , 0:inactivo ')
    
    def  __str__(self):
        return self.nombre
    
    def get_detalle(self):
        return self.detalle
    
    def get_condiciones(self):
        return self.condiciones
    
class UsuarioEncargado(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.PROTECT,related_name='usuario',db_column='usuario')
    encargado = models.ForeignKey(User,on_delete=models.PROTECT,related_name='encargado',db_column='encargado')

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name} - {self.encargado.first_name} {self.encargado.last_name}'
    
    def full_name_usuariopermiso(self):
        return f'{self.usuario.first_name.capitalize()} {self.usuario.last_name.capitalize()}'
    

    def full_name_encargado(self):
        return f'{self.encargado.first_name.capitalize()} {self.encargado.last_name.capitalize()}'
    
class Permisos(models.Model):
    usuariodecreacion = models.ForeignKey(User,on_delete=models.PROTECT,related_name='emails',db_column='emails',null=True,blank=True)
    usuariodepermiso = models.ForeignKey(User,on_delete=models.PROTECT,related_name='usernames',db_column='usernames')
    usuarioaprobacion =  models.ForeignKey(User,on_delete=models.PROTECT,related_name='ids',db_column='ids',null=True,blank=True)
    tipopermiso = models.ForeignKey(Tipodepermiso,on_delete=models.PROTECT)
    beneficio = models.ForeignKey(Beneficios,on_delete=models.PROTECT,null=True,blank=True)
    fechaaprobacion = models.DateTimeField(null=True,blank=True)
    fechaInicial = models.DateTimeField(null=True,blank=False)
    fechaFinal = models.DateTimeField(null=True,blank=False)
    salida = models.DateTimeField(null=True,blank=True)
    reingreso = models.DateTimeField(null=True,blank=True)
    descripcion = models.CharField(null=False,blank=False,max_length=300)
    estado = models.IntegerField(default=0, null=False,help_text='estado 0:solicitado , 1:aprobado , 2: rechazado')
    fechacreacion = models.DateTimeField(null=True,blank=False)
    
    def full_name_usuariopermiso(self):
        return f'{self.usuariodepermiso.first_name.capitalize()} {self.usuariodepermiso.last_name.capitalize()}'

    class Meta:
        permissions = [
        ('ver_permisos_de_todos','ver_permisos_de_todos'),('aprobar_permisos','aprobar_permisos'),
        ('salida_y_entrada','salidad_y_entrada')
        ]


class UsuarioHorarios(models.Model):
    usuario  = models.ForeignKey(User,on_delete=models.PROTECT,related_name='usuariohorarios',db_column='usuario')
    estado = models.IntegerField(default=1, null=False,help_text='estado 1:activo , 0:inactivo')

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name} estado: {self.estado}'


class HorariosPorteria(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.PROTECT,related_name='usuariohorariosporteria',db_column='usuario')
    fecha = models.DateField(null=False,blank=False)
    horaentrada = models.TimeField(null=False,blank=False)
    horasalida = models.TimeField(null=False,blank=False)
    totalhoras = models.FloatField(null=False,blank=False)

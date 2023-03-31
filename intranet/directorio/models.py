from django.db import models

class Sedes(models.Model):
    codigo = models.CharField(null=False,blank=False,max_length=5)
    descripcion= models.CharField(null = False, blank=False,max_length=255)
    
    def __str__(self):
        return self.descripcion.capitalize()
    
    def get_descripcion(self):
        return self.descripcion
    
class Cargos(models.Model):
    codigo = models.IntegerField(blank=False,null=False)
    descripcion = models.CharField(null = False, blank=False,max_length=255)
    
    def __str__(self):
        return  self.descripcion.capitalize()

    def get_descripcion(self):
        return self.descripcion
    
class Ciudades(models.Model):
    codigo = models.IntegerField(blank=False,null=False)
    descripcion = models.CharField(null = False, blank=False,max_length=255)
    
    def __str__(self):
        return self.descripcion.capitalize()
    
    def get_descripcion(self):
        return self.descripcion
    
class Directorio(models.Model):
    sede = models.ForeignKey(Sedes,null=False,blank=False,on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargos,null=True,blank=True,on_delete=models.PROTECT) 
    ciudad = models.ForeignKey(Ciudades,on_delete=models.PROTECT)
    usuario = models.CharField(null=False,blank=False,max_length=255)
    extension = models.CharField(null=True,blank=True,max_length=30)
    telefono = models.CharField(null=True,blank=True,max_length=30)
    email = models.CharField(null=True,blank=True,max_length=255)
    direccion = models.CharField(null=True,blank=True,max_length=255)
    
    def __str__(self):
        return self.usuario +': '+ self.extension +' - '+ self.telefono + ' - '+ self.email
    
    
class Did(models.Model):
    ciudad = models.ForeignKey(Ciudades,on_delete=models.PROTECT)
    indicativo = models.CharField(null=False,blank=False,max_length=5)
    numero = models.CharField(null=False,blank=False,max_length=50)
    
    
class Dir_almacenes(models.Model):
    ciudad = models.ForeignKey(Ciudades,on_delete=models.PROTECT)
    almacen = models.CharField(null=False,blank=False,max_length=200)
    direccion = models.CharField(null=False,blank=False,max_length=200)
    horario = models.CharField(null=False,blank=False,max_length=200)
    telefono = models.CharField(null=False,blank=False,max_length=200)
    correo = models.CharField(null=False,blank=False,max_length=200)
    contacto = models.CharField(null=False,blank=False,max_length=200)
    
    
class Convenios(models.Model):
    nombre = models.CharField(max_length=250)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    activo = models.IntegerField(default=0, null=False,help_text='estado 0: activo , 1: inactivo')
    email = models.EmailField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=30, null=True)
    archivo = models.FileField(upload_to='pdfs/')     
    
class Promociones(models.Model):
    nombre = models.CharField(max_length=250)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    descripcion = models.TextField(max_length=10000)
    banner = models.ImageField(upload_to='imagenes/')
    
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'promociones'
    
    
# Create your models here.

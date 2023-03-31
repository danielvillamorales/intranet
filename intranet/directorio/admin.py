from django.contrib import admin
from directorio.models import *
 
admin.site.register(Convenios)

@admin.register(Did)
class didAdmin(admin.ModelAdmin):
    list_display = ('indicativo', 'numero')
    search_fields = ('indicativo', 'numero')
    list_filter = ('indicativo', 'numero')
    ordering = ('id',)
    
@admin.register(Dir_almacenes)
class diralmAdmin(admin.ModelAdmin):
    list_display = ('almacen', 'correo','telefono')
    search_fields = ('almacen', 'correo','telefono')
    list_filter = ('almacen', 'correo','telefono')
    ordering = ('id',)


@admin.register(Sedes)
class SedesAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    list_filter = ('codigo','descripcion')
    ordering = ('id',)

@admin.register(Cargos)
class cargosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    list_filter = ('codigo','descripcion')
    ordering = ('id',)
    
@admin.register(Ciudades)
class ciudadesAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    list_filter = ('codigo','descripcion')
    ordering = ('id',)
    
@admin.register(Directorio)
class directorioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'extension','telefono','email')
    search_fields = ('usuario', 'extension','telefono','email')
    list_filter = ('usuario', 'extension','telefono','email')
    ordering = ('id',)
# Register your models here.

from django.contrib import admin
from permisos.models import *


# Register your models here.
admin.site.register(Beneficios)
admin.site.register(Tipodepermiso)


@admin.register(Permisos)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('usuariodepermiso','full_name_usuariopermiso', 'tipopermiso','fechaInicial','fechaFinal')
    search_fields = ('usuariodepermiso__username','usuariodepermiso__first_name','usuariodepermiso__last_name')
    ordering = ('-id',)


@admin.register(UsuarioEncargado)
class EncargadoAdmin(admin.ModelAdmin):
    list_display = ('usuario_username', 'full_name_usuariopermiso', 'encargado_username', 'full_name_encargado')
    search_fields = ('usuario__username','usuario__first_name','usuario__last_name','encargado__username','encargado__first_name','encargado__last_name')
    ordering = ('-id',)

    def usuario_username(self, obj):
        return obj.usuario.username
    
    def encargado_username(self, obj):
        return obj.encargado.username
    
admin.site.register(UsuarioHorarios)
@admin.register(HorariosPorteria)
class HorariosPorteriaAdmin(admin.ModelAdmin):
    list_display = ('usuario_username','horaentrada','horasalida', 'tipo', 'diasemana', 'totalhoras')
    search_fields = ('usuario__username','usuario__first_name','usuario__last_name')
    ordering = ('id',)

    def usuario_username(self, obj):
        return f'{obj.usuario.username} {obj.usuario.first_name} {obj.usuario.last_name}' 


    
admin.site.register(CalendarioPorteria)
from django.contrib import admin
from permisos.models import *


# Register your models here.
admin.site.register(Beneficios)
admin.site.register(Tipodepermiso)
admin.site.register(UsuarioEncargado)

@admin.register(Permisos)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('usuariodepermiso', 'tipopermiso','fechaInicial','fechaFinal')
    search_fields = ('usuariodepermiso', 'tipopermiso','fechaInicial','fechaFinal')
    list_filter = ('usuariodepermiso', 'tipopermiso','fechaInicial','fechaFinal')
    ordering = ('id',)
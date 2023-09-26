from django.contrib import admin
from permisos.models import *


# Register your models here.
admin.site.register(Beneficios)
admin.site.register(Tipodepermiso)
admin.site.register(UsuarioEncargado)

@admin.register(Permisos)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('usuariodepermiso','full_name_usuariopermiso', 'tipopermiso','fechaInicial','fechaFinal')
    search_fields = ('usuariodepermiso__username','usuariodepermiso__first_name','usuariodepermiso__last_name')
    ordering = ('-id',)
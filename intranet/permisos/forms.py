from django.forms import ModelForm, EmailInput,TextInput
from permisos.models import *

class PermisosForm(ModelForm):
    class Meta:
        model = Permisos
        fields = ('usuariodepermiso','tipopermiso','beneficio','descripcion')



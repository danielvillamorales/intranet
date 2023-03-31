from django.forms import ModelForm, EmailInput,TextInput
from directorio.models import *

class DirectorioForm(ModelForm):
    class Meta:
        model = Directorio
        fields = '__all__'
        widgets = {
            'email': EmailInput(attrs={'type':'email'})
        }
        
class ArchivoForm(ModelForm):
    class Meta:
        model = Convenios
        fields = ('nombre', 'fecha_inicial', 'fecha_final', 'email', 'telefono', 'archivo')
 
        
class PromocionesForm(ModelForm):
    class Meta:
        model = Promociones
        fields = ('nombre', 'fecha_inicial', 'fecha_final', 'descripcion', 'banner')
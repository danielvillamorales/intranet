from django import forms
from .models import Cajas


class CajasForm(forms.ModelForm):
    class Meta:
        model = Cajas
        fields = ('fecha', 'bodega', 'valor', 'banco', 'observacion','imagen')

    # Define los widgets para cada campo y agrega clases de Bootstrap
    widgets = {
        'fecha': forms.DateInput(attrs={'class': 'form-control'}),
        'bodega': forms.Select(attrs={'class': 'form-control'}),
        'valor': forms.NumberInput(attrs={'class': 'form-control'}),
        'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    }
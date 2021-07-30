from django import forms
from .models import Firma


class FirmaForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome da firma",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Nome da Firma'
            }
        )
    )

    cnpj = forms.CharField(
        required=False,
        label="CNPJ da firma",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'CNPJ da Firma'
            }
        )
    )

    class Meta:
        model = Firma
        fields = [
            'nome', 'cnpj'
        ]
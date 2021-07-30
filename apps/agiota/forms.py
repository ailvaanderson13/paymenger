from django import forms
from .models import Agiota
from apps.firma.models import Firma


class AgiotaForm(forms.ModelForm):
    firma = forms.ModelChoiceField(
        label="Firma",
        queryset=Firma.objects.filter(is_active=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    first_name = forms.CharField(
        label="Primeiro nome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': ' Insira o primeiro nome aqui:'
            }
        )
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': ' Insira o e-mail aqui:'
            }
        )
    )

    celular = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': ' Insira o telefone aqui:'
            }
        )
    )

    class Meta:
        model = Agiota
        fields = [
            'firma', 'first_name', 'email', 'celular'
        ]

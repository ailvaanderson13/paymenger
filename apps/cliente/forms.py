from django import forms
from .models import Cliente
from apps.agiota.models import Agiota


class ClienteForm(forms.ModelForm):
    agiota = forms.ModelChoiceField(
        label="Selecione um Agiota",
        queryset=Agiota.objects.filter(is_active=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    first_name = forms.CharField(
        label="Primeiro nome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o primeiro nome aqui:'
            }
        )
    )

    last_name = forms.CharField(
        label="Sobrenome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o sobrenome aqui:'
            }
        )
    )

    email = forms.CharField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira e-mail aqui:'
            }
        )
    )

    rg = forms.CharField(
        label="RG",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o rg aqui:'
            }
        )
    )

    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o CPF aqui:'
            }
        )
    )

    celular_cliente = forms.CharField(
        label="Celular",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o celular aqui:'
            }
        )
    )

    cep = forms.CharField(
        label="CEP",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o CEP aqui:'
            }
        )
    )

    nome_ref = forms.CharField(
        label="Nome da referência",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o nome aqui:'
            }
        )
    )

    celular_ref = forms.CharField(
        label="Celular da referência",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o celular aqui:'
            }
        )
    )

    rua_ref = forms.CharField(
        label="Rua",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira a rua aqui:'
            }
        )
    )

    num_ref = forms.CharField(
        label="Número",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o número da casa aqui:'
            }
        )
    )

    class Meta:
        model = Cliente
        fields = [
            'agiota', 'first_name', 'last_name', 'email', 'rg', 'cpf', 'celular_cliente', 'cep', 'nome_ref', 'rua_ref',
            'num_ref'
        ]


class ClienteAgiotaForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Primeiro nome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o primeiro nome aqui:'
            }
        )
    )

    last_name = forms.CharField(
        label="Sobrenome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o sobrenome aqui:'
            }
        )
    )

    email = forms.CharField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira e-mail aqui:'
            }
        )
    )

    rg = forms.CharField(
        label="RG",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o rg aqui:'
            }
        )
    )

    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o CPF aqui:'
            }
        )
    )

    celular_cliente = forms.CharField(
        label="Celular",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o celular aqui:'
            }
        )
    )

    cep = forms.CharField(
        label="CEP",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o CEP aqui:'
            }
        )
    )

    nome_ref = forms.CharField(
        label="Nome da referência",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o nome aqui:'
            }
        )
    )

    celular_ref = forms.CharField(
        label="Celular da referência",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o celular aqui:'
            }
        )
    )

    rua_ref = forms.CharField(
        label="Rua",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira a rua aqui:'
            }
        )
    )

    num_ref = forms.CharField(
        label="Número",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Insira o número da casa aqui:'
            }
        )
    )

    class Meta:
        model = Cliente
        fields = [
            'first_name', 'last_name', 'email', 'rg', 'cpf', 'celular_cliente', 'cep', 'nome_ref', 'rua_ref',
            'num_ref'
        ]

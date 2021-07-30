from django import forms
from apps.cliente.models import Cliente
from .choices import JUROS_CHOICES, PARCELAS_CHOICES, DIA_PAGAMENTO_CHOICES
from .models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        label="Selecione o cliente",
        queryset=Cliente.objects.filter(is_active=True),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    valor = forms.CharField(
        label="Valor *",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control req'
            }
        )
    )

    juros = forms.ChoiceField(
        label="Selecione a Taxa de Juros (%) *",
        choices=JUROS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control req'
            }
        )
    )

    parcela = forms.ChoiceField(
        label="Selecione Qtd. de parcelas *",
        choices=PARCELAS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control req'
            }
        )
    )

    vencimento = forms.ChoiceField(
        label="Selecione o dia para vencimento da parcela",
        choices=DIA_PAGAMENTO_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Emprestimo
        fields = [
            'cliente', 'valor', 'juros', 'parcela', 'vencimento'
        ]

from django.db import models
from apps.cliente.models import Cliente
from . import choices
from apps.firma.models import Firma


class Emprestimo(models.Model):
    firma = models.ForeignKey(to=Firma, on_delete=models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(to=Cliente, on_delete=models.DO_NOTHING, blank=True, null=True)
    valor = models.CharField(max_length=6)
    juros = models.CharField(choices=choices.JUROS_CHOICES, max_length=3, default="1")
    parcela = models.CharField(choices=choices.PARCELAS_CHOICES, max_length=3, default="1")
    vencimento = models.CharField(choices=choices.DIA_PAGAMENTO_CHOICES, max_length=3, default="1")
    is_active = models.BooleanField(default=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.valor if self.valor else 'Nenhum'

    class Meta:
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"

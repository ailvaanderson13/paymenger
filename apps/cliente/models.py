from django.db import models
from apps.agiota.models import Agiota


class Cliente(Agiota):
    agiota = models.ForeignKey(to=Agiota, related_name="agiota_cliente", on_delete=models.DO_NOTHING, null=True)
    status = models.BooleanField(default=False)
    rg = models.CharField(max_length=15)
    cpf = models.CharField(max_length=15)
    celular_cliente = models.CharField(max_length=15)
    cep = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    nome_ref = models.CharField(max_length=50)
    rua_ref = models.CharField(max_length=50)
    num_ref = models.CharField(max_length=5)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

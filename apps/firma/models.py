from django.db import models


class Firma(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FIRMA: {self.nome}"

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmas"

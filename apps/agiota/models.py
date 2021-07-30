from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.firma.models import Firma


class Agiota(AbstractUser):
    firma = models.ForeignKey(to=Firma, on_delete=models.DO_NOTHING, null=True, blank=True)
    celular = models.CharField(max_length=15)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.firma}"

    class Meta:
        verbose_name = "Agiota"
        verbose_name_plural = "Agiotas"

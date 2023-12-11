from django.db import models


class TagName(models.TextChoices):
    CASA = "Casa"
    ALIMENTACAO = "Alimentacao"
    SAUDE = "Saude"
    ASSINATURAS = "Assinaturas"
    TRANSPORTE = "Transporte"
    EDUCACAO = "Educacao"
    PET = "Pet"
    LAZER = "Lazer"
    OUTROS = "Outros"


class Tag(models.Model):
    tag_name = models.CharField(
        max_length=70,
        choices=TagName.choices,
    )
    sub_tag_name = models.CharField(max_length=100)

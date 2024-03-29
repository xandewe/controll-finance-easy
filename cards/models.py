from django.db import models
from django.contrib.auth.models import User


class TransactionType(models.TextChoices):
    ACCOUNT = "Account"
    CREDIT_CARD = "Credit"


class Card(models.Model):
    class Meta:
        ordering = ["id"]

    card_name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=TransactionType.choices)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")


class CreditCardDetail(models.Model):
    due_date = models.IntegerField()
    closing_date = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    card = models.OneToOneField(
        "cards.Card", on_delete=models.CASCADE, related_name="card_detail", null=True
    )

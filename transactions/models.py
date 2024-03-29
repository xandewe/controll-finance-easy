from django.db import models
from django.contrib.auth.models import User


class TransactionType(models.TextChoices):
    INCOME = "Income"
    EXPENSE = "Expense"
    PAYMENT = "Payment"


class TransactionStatus(models.TextChoices):
    PENDING = "Pending"
    DONE = "Done"


class Transaction(models.Model):
    class Meta:
        ordering = ["id"]

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100, null=True, blank=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )
    created_at = models.DateField()
    year_month_reference = models.CharField(max_length=7)

    card = models.ForeignKey("cards.Card", on_delete=models.CASCADE, related_name="transactions", default=1)
    tag = models.ForeignKey(
        "tags.Tag", on_delete=models.SET_NULL, related_name="transactions", null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions", default=1
    )

from django.db import models
from django.utils import timezone


class TransactionCategory(models.TextChoices):
    INCOME = "Income"
    EXPENSE = "Expense"
    CREDIT_CARD_EXPENSE = "CREDIT_CARD_EXPENSE"


class TransactionStatus(models.TextChoices):
    PENDING = "Pending"
    DONE = "Done"


class Transaction(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100, null=True)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    category = models.CharField(
        max_length=20,
        choices=TransactionCategory.choices,
    )
    created_at = models.DateField(default=timezone.now)

    tag = models.ForeignKey("tags.Tag", models.PROTECT, related_name="transactions", null=True)

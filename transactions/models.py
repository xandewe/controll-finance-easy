from django.db import models


class TransactionType(models.TextChoices):
    INCOME = "Income"
    EXPENSE = "Expense"
    CREDIT_CARD = "Credit Card"


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

    tag = models.ForeignKey(
        "tags.Tag", models.SET_NULL, related_name="transactions", null=True
    )

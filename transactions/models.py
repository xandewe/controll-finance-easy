from django.db import models


class TransactionCategory(models.TextChoices):
    INCOME = "Income"
    EXPENSE = "Expense"


class TransactionStatus(models.TextChoices):
    PENDING = "Pending"
    DONE = "Done"


class Transaction(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=100, null=True)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    credit_card = models.BooleanField(default=True)
    category = models.CharField(
        max_length=20,
        choices=TransactionCategory.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ForeignKey("tags.Tag", models.PROTECT, related_name="transactions")

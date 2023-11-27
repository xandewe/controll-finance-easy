from django.db import models


class CategoryChoice(models.TextChoices):
    INCOME = "income"
    EXPENSE = "Expense"
    UNDEFINED = "Undefined"


class Transaction(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(
        max_length=100,
        null=True
    )  # colocar como não obrigatório
    value = models.DecimalField(max_digits=5, decimal_places=2)
    received = models.BooleanField(default=True)
    credit_card = models.BooleanField(default=True)
    category = models.CharField(
        max_length=20, choices=CategoryChoice.choices, default=CategoryChoice.UNDEFINED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField("tags.Tag", related_name="transactions")

# Generated by Django 4.2.7 on 2023-11-29 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='credit_card',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense'), ('CREDIT_CARD_EXPENSE', 'Credit Card Expense')], max_length=20),
        ),
    ]

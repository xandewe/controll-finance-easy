# Generated by Django 4.2.7 on 2024-01-10 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_options_alter_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='month_year_reference',
            field=models.CharField(default='2023-01', max_length=6),
        ),
    ]
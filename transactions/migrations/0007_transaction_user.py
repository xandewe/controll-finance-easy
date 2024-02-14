# Generated by Django 4.2.7 on 2024-01-31 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0006_alter_transaction_year_month_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL),
        ),
    ]

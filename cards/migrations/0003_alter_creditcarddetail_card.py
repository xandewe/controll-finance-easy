# Generated by Django 4.2.7 on 2024-02-21 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_alter_card_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcarddetail',
            name='card',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_detail', to='cards.card'),
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-08 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['id']},
        ),
    ]

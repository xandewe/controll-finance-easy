# Generated by Django 4.2.7 on 2023-12-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='sub_tag_name',
            field=models.CharField(max_length=100),
        ),
    ]

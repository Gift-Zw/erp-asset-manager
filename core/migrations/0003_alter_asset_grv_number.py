# Generated by Django 4.1.3 on 2023-02-19 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_repair_currency_disposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='grv_number',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

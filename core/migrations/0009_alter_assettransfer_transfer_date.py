# Generated by Django 4.1.3 on 2023-07-25 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_assettransfer_transfer_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettransfer',
            name='transfer_date',
            field=models.DateField(),
        ),
    ]

# Generated by Django 4.1.3 on 2023-07-25 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_assetdisposal_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='assettransfer',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]

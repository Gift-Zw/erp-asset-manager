# Generated by Django 4.1.3 on 2023-07-31 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_assettransfer_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetdisposal',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assetrepair',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]

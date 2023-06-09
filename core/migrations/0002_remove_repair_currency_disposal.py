# Generated by Django 4.1.3 on 2023-02-18 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repair',
            name='currency',
        ),
        migrations.CreateModel(
            name='Disposal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('remarks', models.TextField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='disposal', to='core.asset')),
            ],
        ),
    ]

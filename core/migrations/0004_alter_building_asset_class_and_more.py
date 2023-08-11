# Generated by Django 4.1.3 on 2023-06-20 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_building_asset_class_equipment_asset_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
        migrations.AlterField(
            model_name='furniture',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
        migrations.AlterField(
            model_name='land',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
        migrations.AlterField(
            model_name='machinery',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
        migrations.AlterField(
            model_name='motorvehicle',
            name='asset_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.assetclassproperties'),
        ),
    ]

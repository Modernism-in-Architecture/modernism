# Generated by Django 3.1.13 on 2021-10-23 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mia_buildings", "0002_auto_20211023_1733"),
    ]

    operations = [
        migrations.RenameField(
            model_name="building",
            old_name="building_type",
            new_name="building_types",
        ),
    ]

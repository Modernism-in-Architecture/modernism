# Generated by Django 4.2.11 on 2024-10-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mia_buildings", "0025_remove_building_thumbnails_created_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buildingimage",
            name="thumbnails_created",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
# Generated by Django 3.1.13 on 2021-10-24 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mia_buildings", "0007_auto_20211024_0023"),
    ]

    operations = [
        migrations.AddField(
            model_name="building",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.22 on 2025-07-11 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mia_general', '__first__'),
        ('mia_buildings', '0027_remove_building_published_on_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingimage',
            name='todo_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mia_general.todoitem'),
        ),
    ]

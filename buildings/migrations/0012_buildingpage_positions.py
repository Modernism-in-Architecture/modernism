# Generated by Django 3.1.8 on 2021-05-13 20:06

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0011_constructiontype_detail_facade_position_roof_window'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingpage',
            name='positions',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='buildings.Position'),
        ),
    ]
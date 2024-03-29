# Generated by Django 3.1.13 on 2021-10-25 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mia_people", "0002_person_place_of_death"),
    ]

    operations = [
        migrations.AddField(
            model_name="architect",
            name="architect_mentors",
            field=models.ManyToManyField(
                blank=True,
                related_name="_architect_architect_mentors_+",
                to="mia_people.Architect",
            ),
        ),
        migrations.AddField(
            model_name="architect",
            name="professor_mentors",
            field=models.ManyToManyField(blank=True, to="mia_people.Professor"),
        ),
        migrations.AlterField(
            model_name="professor",
            name="architect_mentors",
            field=models.ManyToManyField(blank=True, to="mia_people.Architect"),
        ),
    ]

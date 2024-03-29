# Generated by Django 3.1.13 on 2021-10-23 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mia_facts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccessType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Access types",
            },
        ),
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=250, unique=True)),
                ("subtitle", models.CharField(blank=True, max_length=250)),
                ("todays_use", models.CharField(blank=True, max_length=300)),
                ("year_of_construction", models.CharField(blank=True, max_length=4)),
                ("history", models.TextField(blank=True)),
                ("description", models.TextField(blank=True)),
                ("directions", models.TextField(blank=True)),
                ("address", models.TextField(blank=True)),
                ("zip_code", models.CharField(default="00000", max_length=16)),
                ("latitude", models.DecimalField(decimal_places=20, max_digits=23)),
                ("longitude", models.DecimalField(decimal_places=20, max_digits=23)),
                ("protected_monument", models.BooleanField(default=False)),
                ("storey", models.IntegerField(blank=True, null=True)),
                (
                    "access_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="mia_buildings.accesstype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BuildingType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name_plural": "Building types",
            },
        ),
        migrations.CreateModel(
            name="ConstructionType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Detail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Facade",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Roof",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Window",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BuildingImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="mia-buildings"),
                ),
                ("is_feed_image", models.BooleanField(default=False)),
                ("title", models.CharField(blank=True, max_length=250)),
                ("photographer", models.CharField(blank=True, max_length=250)),
                ("description", models.TextField(blank=True)),
                (
                    "building",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="mia_buildings.building",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="building",
            name="building_type",
            field=models.ManyToManyField(blank=True, to="mia_buildings.BuildingType"),
        ),
        migrations.AddField(
            model_name="building",
            name="city",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="mia_facts.city",
            ),
        ),
        migrations.AddField(
            model_name="building",
            name="construction_types",
            field=models.ManyToManyField(
                blank=True, to="mia_buildings.ConstructionType"
            ),
        ),
        migrations.AddField(
            model_name="building",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="mia_facts.country",
            ),
        ),
        migrations.AddField(
            model_name="building",
            name="details",
            field=models.ManyToManyField(blank=True, to="mia_buildings.Detail"),
        ),
        migrations.AddField(
            model_name="building",
            name="facades",
            field=models.ManyToManyField(blank=True, to="mia_buildings.Facade"),
        ),
        migrations.AddField(
            model_name="building",
            name="positions",
            field=models.ManyToManyField(blank=True, to="mia_buildings.Position"),
        ),
        migrations.AddField(
            model_name="building",
            name="roofs",
            field=models.ManyToManyField(blank=True, to="mia_buildings.Roof"),
        ),
        migrations.AddField(
            model_name="building",
            name="windows",
            field=models.ManyToManyField(blank=True, to="mia_buildings.Window"),
        ),
    ]

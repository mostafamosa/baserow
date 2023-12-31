# Generated by Django 2.2.11 on 2020-05-26 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0006_auto_20200522_1329"),
    ]

    operations = [
        migrations.CreateModel(
            name="DateField",
            fields=[
                (
                    "field_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.Field",
                    ),
                ),
                (
                    "date_format",
                    models.CharField(
                        choices=[
                            ("EU", "European (D/M/Y)"),
                            ("US", "US (M/D/Y)"),
                            ("ISO", "ISO (Y-M-D)"),
                        ],
                        default=("EU", "European (D/M/Y)"),
                        max_length=32,
                    ),
                ),
                ("date_include_time", models.BooleanField(default=False)),
                (
                    "date_time_format",
                    models.CharField(
                        choices=[("24", "24 hour"), ("12", "12 hour")],
                        default=("24", "24 hour"),
                        max_length=32,
                    ),
                ),
            ],
            bases=("database.field",),
        ),
    ]

# Generated by Django 3.2.12 on 2022-05-02 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0069_view_trashed"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrashedRows",
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
                ("row_ids", models.JSONField()),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="database.table"
                    ),
                ),
            ],
        ),
    ]

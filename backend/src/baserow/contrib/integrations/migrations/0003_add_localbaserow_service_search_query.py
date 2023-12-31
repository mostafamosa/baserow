# Generated by Django 3.2.20 on 2023-09-11 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0002_migrate_localbaserow_to_views"),
    ]

    operations = [
        migrations.AddField(
            model_name="localbaserowgetrow",
            name="search_query",
            field=models.TextField(
                default="",
                help_text="The query to apply to the service to narrow the results down.",
                max_length=225,
            ),
        ),
        migrations.AddField(
            model_name="localbaserowlistrows",
            name="search_query",
            field=models.TextField(
                default="",
                help_text="The query to apply to the service to narrow the results down.",
                max_length=225,
            ),
        ),
    ]

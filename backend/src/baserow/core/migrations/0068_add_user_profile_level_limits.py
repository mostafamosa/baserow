# Generated by Django 3.2.18 on 2023-04-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0067_alter_settings_track_workspace_usage"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="concurrency_limit",
            field=models.SmallIntegerField(
                blank=True,
                default=None,
                help_text="An optional per user concurrency limit.",
                null=True,
            ),
        ),
    ]

# Generated by Django 3.2.13 on 2022-07-20 16:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0081_batch_webhooks"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileimportjob",
            name="user_websocket_id",
            field=models.CharField(
                help_text="The user websocket uuid needed to manage signals sent "
                "correctly.",
                max_length=36,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="fileimportjob",
            name="user_session_id",
            field=models.CharField(
                help_text="The user session uuid needed for undo/redo functionality.",
                max_length=36,
                null=True,
            ),
        ),
    ]

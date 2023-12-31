# Generated by Django 3.2.18 on 2023-07-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0072_notifications"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="notificationrecipient",
            name="unread_notif_count_idx",
        ),
        migrations.AddField(
            model_name="notificationrecipient",
            name="queued",
            field=models.BooleanField(
                default=False,
                help_text="If True, then the notification has been queued for sending. Queued notifications cannot be seen by the user yet. Once the notification has been sent, this field will be set to False and the user will be able to fetch it via API.",
            ),
        ),
        migrations.AddIndex(
            model_name="notificationrecipient",
            index=models.Index(
                condition=models.Q(("cleared", False), ("read", False)),
                fields=[
                    "broadcast",
                    "cleared",
                    "read",
                    "queued",
                    "recipient_id",
                    "workspace_id",
                ],
                include=("notification_id",),
                name="unread_notif_count_idx",
            ),
        ),
    ]

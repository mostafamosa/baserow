# Generated by Django 3.2.6 on 2021-11-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0044_field_dependencies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]

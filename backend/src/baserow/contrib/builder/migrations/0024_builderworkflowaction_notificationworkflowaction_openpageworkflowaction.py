# Generated by Django 3.2.21 on 2023-10-05 11:14

import django.db.models.deletion
from django.db import migrations, models

import baserow.core.fields
import baserow.core.formula.field
import baserow.core.mixins


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("builder", "0023_headingelement_font_color"),
    ]

    operations = [
        migrations.CreateModel(
            name="BuilderWorkflowAction",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", baserow.core.fields.SyncedDateTimeField(auto_now=True)),
                (
                    "event",
                    models.CharField(
                        choices=[("click", "Click")],
                        help_text="The event that triggers the execution",
                        max_length=30,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="builder_workflow_actions",
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
                (
                    "element",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="builder.element",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="builder.page"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                baserow.core.mixins.PolymorphicContentTypeMixin,
                baserow.core.mixins.OrderableMixin,
                models.Model,
                baserow.core.mixins.WithRegistry,
            ),
        ),
        migrations.CreateModel(
            name="NotificationWorkflowAction",
            fields=[
                (
                    "builderworkflowaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="builder.builderworkflowaction",
                    ),
                ),
                ("title", baserow.core.formula.field.FormulaField(default="")),
                ("description", baserow.core.formula.field.FormulaField(default="")),
            ],
            options={
                "abstract": False,
            },
            bases=("builder.builderworkflowaction",),
        ),
        migrations.CreateModel(
            name="OpenPageWorkflowAction",
            fields=[
                (
                    "builderworkflowaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="builder.builderworkflowaction",
                    ),
                ),
                ("url", baserow.core.formula.field.FormulaField(default="")),
            ],
            options={
                "abstract": False,
            },
            bases=("builder.builderworkflowaction",),
        ),
    ]

from django.utils.functional import lazy
from rest_framework import serializers

from baserow.contrib.database.views.models import (
    ViewFilter,
    FILTER_TYPES,
)
from baserow.contrib.database.views.registries import (
    view_filter_type_registry,
)


class SelectColorValueProviderConfSerializer(serializers.Serializer):
    field_id = serializers.IntegerField(
        allow_null=True,
        help_text=(
            "An id of a select field of the table. "
            "The value provider return the color of the selected option for each row."
        ),
    )


class ConditionalColorValueProviderConfColorFilterSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="A unique identifier for this condition.")
    field = serializers.IntegerField(
        allow_null=True,
        help_text=ViewFilter._meta.get_field("field").help_text,
    )
    type = serializers.ChoiceField(
        choices=lazy(view_filter_type_registry.get_types, list)(),
        allow_null=True,
        help_text=ViewFilter._meta.get_field("type").help_text,
    )
    value = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text=ViewFilter._meta.get_field("field").help_text,
    )


class ConditionalColorValueProviderConfColorSerializer(serializers.Serializer):
    color = serializers.CharField(
        help_text="The color the decorator should take if the defined conditions apply."
    )
    filters = ConditionalColorValueProviderConfColorFilterSerializer(
        many=True,
        help_text=(
            "A list of conditions that the row must meet to get the selected color. "
            "This list of conditions can be empty, in that case, "
            "this color will always match the row values."
        ),
    )
    operator = serializers.ChoiceField(
        choices=FILTER_TYPES,
        default="AND",
        help_text="The boolean operator used to group all conditions.",
    )


class ConditionalColorValueProviderConfColorsSerializer(serializers.Serializer):
    colors = ConditionalColorValueProviderConfColorSerializer(
        many=True,
        help_text=(
            "A list of color items. For each row, the value provider try to "
            "match the defined colors one by one in the given order. "
            "The first matching color is returned to the decorator."
        ),
    )

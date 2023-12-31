from unittest.mock import MagicMock

import pytest

from baserow.contrib.builder.data_providers.data_provider_types import (
    DataSourceDataProviderType,
    PageParameterDataProviderType,
)
from baserow.contrib.builder.data_sources.builder_dispatch_context import (
    BuilderDispatchContext,
)
from baserow.core.services.dispatch_context import DispatchContext
from baserow.core.services.exceptions import ServiceImproperlyConfigured


class FakeDispatchContext(DispatchContext):
    def __init__():
        super().__init__()

    def range(self, service):
        return [0, 100]

    def __getitem__(self, key: str):
        if key == "test":
            return 2
        if key == "test1":
            return 1
        if key == "test2":
            return ""
        if key == "test999":
            return "999"

        return super().__getitem__(key)


def test_page_parameter_data_provider_get_data_chunk():
    page_parameter_provider = PageParameterDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {"page_parameter": {"id": 42}}

    dispatch_context = BuilderDispatchContext(fake_request, None)

    assert page_parameter_provider.get_data_chunk(dispatch_context, ["id"]) == 42
    assert page_parameter_provider.get_data_chunk(dispatch_context, []) is None
    assert (
        page_parameter_provider.get_data_chunk(dispatch_context, ["id", "test"]) is None
    )
    assert page_parameter_provider.get_data_chunk(dispatch_context, ["test"]) is None


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk(data_fixture):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="2",
        name="Item",
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()

    dispatch_context = BuilderDispatchContext(fake_request, page)

    assert (
        data_source_provider.get_data_chunk(
            dispatch_context, [data_source.id, fields[1].db_column]
        )
        == "Orange"
    )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula(data_fixture):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="get('page_parameter.id')",
        name="Item",
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {"id": 2},
    }

    dispatch_context = BuilderDispatchContext(fake_request, page)

    assert (
        data_source_provider.get_data_chunk(
            dispatch_context, [data_source.id, fields[1].db_column]
        )
        == "Orange"
    )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula_using_datasource(
    data_fixture,
):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    table2, fields2, rows2 = data_fixture.build_table(
        user=user,
        columns=[
            ("Id", "text"),
        ],
        rows=[
            ["1"],
            ["2"],
            ["3"],
            ["3"],
        ],
    )
    view2 = data_fixture.create_grid_view(user, table=table2)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view2,
        table=table2,
        row_id="get('page_parameter.id')",
        name="Id source",
    )
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id=f"get('data_source.{data_source2.id}.{fields2[0].db_column}')",
        name="Item",
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {"id": 2},
    }

    dispatch_context = BuilderDispatchContext(fake_request, page)

    assert (
        data_source_provider.get_data_chunk(
            dispatch_context, [data_source.id, fields[1].db_column]
        )
        == "Orange"
    )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula_to_missing_datasource(
    data_fixture,
):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    table2, fields2, rows2 = data_fixture.build_table(
        user=user,
        columns=[
            ("Id", "text"),
        ],
        rows=[
            ["1"],
            ["2"],
            ["3"],
            ["3"],
        ],
    )
    view2 = data_fixture.create_grid_view(user, table=table2)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="get('data_source.99999.Id')",
        name="Item",
    )

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {},
    }

    dispatch_context = BuilderDispatchContext(fake_request, page)

    with pytest.raises(ServiceImproperlyConfigured):
        data_source_provider.get_data_chunk(
            dispatch_context, [data_source.id, fields[1].db_column]
        )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula_recursion(
    data_fixture,
):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    table2, fields2, rows2 = data_fixture.build_table(
        user=user,
        columns=[
            ("Id", "text"),
        ],
        rows=[
            ["1"],
            ["2"],
            ["3"],
            ["3"],
        ],
    )
    view2 = data_fixture.create_grid_view(user, table=table2)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="",
        name="Item",
    )

    data_source.row_id = f"get('data_source.{data_source.id}.Id')"
    data_source.save()

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {},
    }

    dispatch_context = BuilderDispatchContext(fake_request, page)

    with pytest.raises(ServiceImproperlyConfigured):
        data_source_provider.get_data_chunk(
            dispatch_context, [data_source.id, fields[1].db_column]
        )


@pytest.mark.django_db
def test_data_source_data_provider_get_data_chunk_with_formula_using_datasource_calling_each_others(
    data_fixture,
):
    user = data_fixture.create_user()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["Volkswagen", "White"],
            ["Volkswagen", "Green"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    table2, fields2, rows2 = data_fixture.build_table(
        user=user,
        columns=[
            ("Id", "text"),
        ],
        rows=[
            ["1"],
            ["2"],
            ["3"],
            ["3"],
        ],
    )
    view2 = data_fixture.create_grid_view(user, table=table2)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="",
        name="Item",
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view2,
        table=table2,
        row_id=f"get('data_source.{data_source.id}.Id')",
        name="Id source",
    )

    data_source.row_id = f"get('data_source.{data_source2.id}.Id')"
    data_source.save()

    data_source_provider = DataSourceDataProviderType()

    fake_request = MagicMock()
    fake_request.data = {
        "data_source": {"page_id": page.id},
        "page_parameter": {},
    }

    dispatch_context = BuilderDispatchContext(fake_request, page)

    with pytest.raises(ServiceImproperlyConfigured):
        data_source_provider.get_data_chunk(
            dispatch_context, [data_source.id, fields[1].db_column]
        )

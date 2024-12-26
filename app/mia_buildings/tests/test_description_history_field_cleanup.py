import pytest

from mia_buildings.admin_forms import BuildingAdminForm


@pytest.mark.django_db
def test_clean_description_and_history_valid_data():
    # GIVEN
    form_data = {
        "name": "A building",
        "description": "<p>Valid description</p>",
        "history": "<p>Valid history</p>",
    }

    # WHEN
    form = BuildingAdminForm(data=form_data)

    # THEN
    assert form.is_valid()
    assert form.clean_description() == "<p>Valid description</p>"
    assert form.clean_history() == "<p>Valid history</p>"


@pytest.mark.parametrize(
    "history_data, description_data, error_fields, clean_fields",
    [
        (
            "Invalid <script>alert('Hello');</script> history",
            "Invalid <script>alert('Hello');</script> description",
            ["history", "description"],
            [],
        ),
        (
            "Invalid <script>alert('Hello');</script> history",
            "<p>Valid description</p>",
            ["history"],
            ["description"],
        ),
        (
            "<p>Valid history</p>",
            "Invalid <script>alert('Hello');</script> description",
            ["description"],
            ["history"],
        ),
    ],
)
@pytest.mark.django_db
def test_clean_description_and_history_invalid_data(
    history_data, description_data, error_fields, clean_fields
):
    # GIVEN
    form_data = {
        "title": "A fact",
        "description": description_data,
        "history": history_data,
    }

    # WHEN
    form = BuildingAdminForm(data=form_data)

    # THEN
    assert not form.is_valid()
    for error_field in error_fields:
        assert error_field in form.errors
    for clean_field in clean_fields:
        assert clean_field not in form.errors

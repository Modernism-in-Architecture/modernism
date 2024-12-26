import pytest

from mia_people.admin_forms import (
    ArchitectAdminForm,
    DeveloperAdminForm,
    ProfessorAdminForm,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "admin_form", [DeveloperAdminForm, ArchitectAdminForm, ProfessorAdminForm]
)
def test_clean_description_valid_data(admin_form):
    # GIVEN
    form_data = {
        "last_name": "A last name",
        "description": "<p>Valid description</p>",
    }

    # WHEN
    form = admin_form(data=form_data)

    # THEN
    assert form.is_valid()
    assert form.clean_description() == "<p>Valid description</p>"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "admin_form", [DeveloperAdminForm, ArchitectAdminForm, ProfessorAdminForm]
)
def test_clean_description_invalid_data(admin_form):
    # GIVEN
    form_data = {
        "last_name": "A last name",
        "description": "Invalid <script>alert('Hello');</script> description",
    }

    # WHEN
    form = admin_form(data=form_data)

    # THEN
    assert not form.is_valid()
    assert "description" in form.errors

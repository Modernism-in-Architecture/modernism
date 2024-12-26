import pytest

from mia_facts.admin_forms import FactAdminForm


@pytest.mark.django_db
def test_clean_description_valid_data():
    # GIVEN
    form_data = {
        "title": "A fact",
        "description": "<p>Valid description</p>",
    }

    # WHEN
    form = FactAdminForm(data=form_data)

    # THEN
    assert form.is_valid()
    assert form.clean_description() == "<p>Valid description</p>"


@pytest.mark.django_db
def test_clean_description_invalid_data():
    # GIVEN
    form_data = {
        "title": "A fact",
        "description": "Invalid <script>alert('Hello');</script> description",
    }

    # WHEN
    form = FactAdminForm(data=form_data)

    # THEN
    assert not form.is_valid()
    assert "description" in form.errors

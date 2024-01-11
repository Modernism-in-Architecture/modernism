import pytest

from mia_buildings.admin_utils import validate_and_clean_content_markup


def test_validate_and_clean_markup_empty_strings():
    # GIVEN
    given_data = ""

    # WHEN
    clean, cleaned_data = validate_and_clean_content_markup()

    # THEN
    assert clean is False
    assert cleaned_data == ""



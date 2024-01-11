import pytest
from mia_buildings.admin_utils import validate_and_clean_content_markup


def test_validate_and_clean_markup_empty_string():
    # GIVEN
    given_data = ""

    # WHEN
    was_cleaned, cleaned_data = validate_and_clean_content_markup(given_data)

    # THEN
    assert was_cleaned is True
    assert cleaned_data == ""


@pytest.mark.parametrize(
    "given_data, expected_was_clean, expected_cleaned_data",
    [
        (
            '<pre id="tw-rmn" class="tw-data-placeholder" dir="ltr" style="text-align: left;" data-placeholder=""></pre>',
            False,
            "",
        ),
        (
            '<p id="tw-target-text" class="tw-data-text" dir="ltr" style="text-align: left;" data-placeholder="&Uuml;bersetzung"><span class="Y2IQFc" lang="en">Ritter designed the houses fundamentally differently<span class="label label-primary"></span></div>',
            False,
            "<p>Ritter designed the houses fundamentally differently</p>",
        ),
        (
            '<p data-block-key="5ti6e">The architect Otto Hellriegel was a member</p><p data-block-key="556f9">On this <a href="https://momentmaschine.de/bauhaus-leipzig/">website</a>',
            False,
            '<p>The architect Otto Hellriegel was a member</p><p>On this <a href="https://momentmaschine.de/bauhaus-leipzig/">website</a></p>',
        ),
        (
            "<p>The sliding windows of some rooms are rarely found in Leipzig.</p><br /><p>He never returned to Brno.</p>",
            False,
            "<p>The sliding windows of some rooms are rarely found in Leipzig.</p><p>He never returned to Brno.</p>",
        ),
        (
            "<p>The sliding <em>windows</em> of some rooms are rarely found in <strong>Leipzig</strong>.</p><br /><p>He <b>never</b> returned to Brno.</p>",
            False,
            "<p>The sliding <em>windows</em> of some rooms are rarely found in <strong>Leipzig</strong>.</p><p>He never returned to Brno.</p>",
        ),
        (
            "<p>The sliding <em>windows</em> of some rooms are rarely found in <strong>Leipzig</strong>.</p><p>He never returned to Brno.</p>",
            True,
            "<p>The sliding <em>windows</em> of some rooms are rarely found in <strong>Leipzig</strong>.</p><p>He never returned to Brno.</p>",
        ),
    ],
)
def test_validate_and_clean_markup(
    given_data, expected_was_clean, expected_cleaned_data
):
    # WHEN
    was_clean, cleaned_data = validate_and_clean_content_markup(given_data)

    # THEN
    assert was_clean == expected_was_clean
    assert cleaned_data == expected_cleaned_data

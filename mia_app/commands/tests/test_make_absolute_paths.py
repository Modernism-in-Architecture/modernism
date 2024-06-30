from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase

from commands.management.commands.make_absolute_paths import Command as ReplaceCommand
from mia_buildings.tests.factories import BuildingFactory


HTML_WITH_RELATIVE_PATH = (
    f"The construction time for this school is mentioned 1931. It might be possible, "
    f"that the construction works started in 1930. The regional government of Merseburg "
    f"showed interest in modern architecture. Not far away in "
    f"<a href='../../../../../buildings/elementary-school-grundschule-wettin/' target='_blank' rel='noopener'>Wettin</a> "
    f"was built a school in 1931."
)
HTML_WITHOUT_RELATIVE_PATH = (
    f"<p>The construction time for this school is mentioned 1931. It might be possible, "
    f"that the <b>construction works started in 1930</b>. The regional government of Merseburg "
    f"showed interest in modern architecture. Not far away in "
    f"was built a school in 1931.</p>"
)


class MakeAbsolutePathsUnitTests(SimpleTestCase):
    def test_relative_path_is_replaced_by_base_url(self):
        result = ReplaceCommand().substitute_relative_paths(
            "<a href='../../../../../buildings/elementary-school-grundschule-wettin/'>Wettin</a>"
        )
        self.assertEqual(
            result,
            f"<a href='{settings.BASE_URL}/buildings/elementary-school-grundschule-wettin/'>Wettin</a>",
        )

        result = ReplaceCommand().substitute_relative_paths(
            "<a href='../../../../buildings/elementary-school-grundschule-wettin/'>Wettin</a>"
        )
        self.assertEqual(
            result,
            f"<a href='{settings.BASE_URL}/buildings/elementary-school-grundschule-wettin/'>Wettin</a>",
        )

    def test_only_relative_paths_in_links_are_replaced(self):
        result = ReplaceCommand().substitute_relative_paths(
            "something '../../../../../buildings/elementary-school-grundschule-wettin/' something else"
        )
        self.assertEqual(
            result,
            "something '../../../../../buildings/elementary-school-grundschule-wettin/' something else",
        )

    def test_relative_paths_with_other_debths_are_ignored(self):
        result = ReplaceCommand().substitute_relative_paths(
            "<a href='../../buildings/elementary-school-grundschule-wettin/'>Wettin</a>"
        )
        self.assertEqual(
            result,
            "<a href='../../buildings/elementary-school-grundschule-wettin/'>Wettin</a>",
        )

        result = ReplaceCommand().substitute_relative_paths(
            "<a href='../../../../../../../../buildings/elementary-school-grundschule-wettin/'>Wettin</a>"
        )
        self.assertEqual(
            result,
            "<a href='../../../../../../../../buildings/elementary-school-grundschule-wettin/'>Wettin</a>",
        )

    def test_relative_paths_are_replaced_if_double_quotes(self):
        result = ReplaceCommand().substitute_relative_paths(
            '<a href="../../../../../buildings/elementary-school-grundschule-wettin/">Wettin</a>'
        )
        self.assertEqual(
            result,
            f'<a href="{settings.BASE_URL}/buildings/elementary-school-grundschule-wettin/">Wettin</a>',
        )

    def test_other_links_are_ignored(self):
        result = ReplaceCommand().substitute_relative_paths(
            '<a href="https://wettin.org">Wettin</a>'
        )
        self.assertEqual(
            result,
            f'<a href="https://wettin.org">Wettin</a>',
        )


class MakeAbsolutePathsTests(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "make_absolute_paths",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_make_absolute_paths_dry_run_mode(self):
        # GIVEN
        building = BuildingFactory(
            description=HTML_WITH_RELATIVE_PATH, history=HTML_WITH_RELATIVE_PATH
        )

        # WHEN
        out = self.call_command()

        # THEN
        building.refresh_from_db()
        self.assertEqual(out, "In dry run mode (--update not passed)\n")
        self.assertEqual(building.description, HTML_WITH_RELATIVE_PATH)
        self.assertEqual(building.history, HTML_WITH_RELATIVE_PATH)

    def test_make_absolute_paths_with_update_flag_if_fields_are_empty(self):
        # GIVEN
        building = BuildingFactory(description="", history="")

        # WHEN
        out = self.call_command("--update")

        # THEN
        building.refresh_from_db()
        self.assertEqual(building.description, "")
        self.assertEqual(building.history, "")

    def test_make_absolute_paths_with_update_flag(self):
        # GIVEN
        building_a = BuildingFactory(
            description=HTML_WITH_RELATIVE_PATH, history=HTML_WITH_RELATIVE_PATH
        )
        building_b = BuildingFactory(
            description=HTML_WITHOUT_RELATIVE_PATH, history=HTML_WITHOUT_RELATIVE_PATH
        )

        expected_html = (
            f"The construction time for this school is mentioned 1931. "
            f"It might be possible, that the construction works started in 1930. "
            f"The regional government of Merseburg showed interest in modern architecture. Not far away in "
            f"<a href='{settings.BASE_URL}/buildings/elementary-school-grundschule-wettin/' target='_blank' rel='noopener'>Wettin</a> was built a school in 1931."
        )

        # WHEN
        out = self.call_command("--update")

        # THEN
        building_a.refresh_from_db()
        building_b.refresh_from_db()
        self.assertEqual(building_a.description, expected_html)
        self.assertEqual(building_a.history, expected_html)
        self.assertEqual(building_b.description, HTML_WITHOUT_RELATIVE_PATH)
        self.assertEqual(building_b.history, HTML_WITHOUT_RELATIVE_PATH)

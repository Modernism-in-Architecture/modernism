from unittest import skip

from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase

from .factories import ArchitectPageFactory, BuildingPageFactory, DeveloperPageFactory


class TestMigrations(TestCase):
    # Setup taken from https://www.caktusgroup.com/blog/2016/02/02/writing-unit-tests-django-migrations/

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert (
            self.migrate_from and self.migrate_to
        ), f"TestCase '{type(self).__name__}' must define migrate_from and migrate_to properties"

        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class PeopleMigrationCase(TestMigrations):

    migrate_from = "0014_auto_20210807_0843"
    migrate_to = "0015_add_architects_developers"

    def setUpBeforeMigration(self, apps):
        building = BuildingPageFactory()
        architect_a = ArchitectPageFactory()
        architect_b = ArchitectPageFactory()
        developer_a = DeveloperPageFactory()
        BuildingPageArchitectRelation = apps.get_model(
            "buildings", "BuildingPageArchitectRelation"
        )
        BuildingPageDeveloperRelation = apps.get_model(
            "buildings", "BuildingPageDeveloperRelation"
        )
        BuildingPageArchitectRelation(architect=architect_a, page=building)
        BuildingPageArchitectRelation(architect=architect_b, page=building)
        BuildingPageDeveloperRelation(developer=developer_a, page=building)

        self.building_id = building.id

    @skip("Outdated, models have been deleted.")
    def test_people_migrated(self):
        BuildingPage = apps.get_model("buildings", "BuildingPage")
        building = BuildingPage.objects.get(id=self.building_id)

        self.assertEqual(building.related_architects.count(), 2)
        self.assertEqual(building.related_developers.count(), 1)

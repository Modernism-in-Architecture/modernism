from django.utils import timezone
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from mia_buildings.tests.factories import BuildingFactory
from mia_facts.tests.factories import CityFactory
from mia_people.tests.factories import ArchitectFactory
from django.test.utils import ignore_warnings

ignore_warnings(message="No directory at", module="whitenoise.base").enable()


class TwitterBuildingAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            "admin", "admin@example.com", "admin123"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_building_details_200(self) -> None:
        # GIVEN
        city = CityFactory()
        building_a = BuildingFactory(
            city=city,
            is_published=True,
            published_on_twitter=timezone.now() - timezone.timedelta(days=1),
        )
        building_b = BuildingFactory(city=city, is_published=True)

        # WHEN
        url = f"/api/v1/twitter/get_building_details/"
        response = self.client.get(url)

        # THEN
        self.assertEqual(200, response.status_code)

        building_data = response.json().get("data")
        building_data_dict_keys = building_data.keys()

        self.assertTrue(len(building_data), 1)
        self.assertTrue("id" in building_data_dict_keys)
        self.assertTrue("name" in building_data_dict_keys)
        self.assertTrue("yearOfConstruction" in building_data_dict_keys)
        self.assertTrue("city" in building_data_dict_keys)
        self.assertTrue("country" in building_data_dict_keys)
        self.assertTrue("architect" in building_data_dict_keys)
        self.assertTrue("absoluteURL" in building_data_dict_keys)
        self.assertNotEqual(building_a.id, building_data.get("id"))
        self.assertEqual(building_b.id, building_data.get("id"))

    def test_latest_building_is_returned(self) -> None:
        # GIVEN
        city = CityFactory()
        BuildingFactory(city=city, is_published=True)
        latest_building = BuildingFactory(city=city, is_published=True)

        # WHEN
        url = f"/api/v1/twitter/get_building_details/"
        response = self.client.get(url)

        # THEN
        self.assertEqual(200, response.status_code)
        building_data = response.json().get("data")
        self.assertEqual(building_data.get("id"), latest_building.id)

    def test_unpublished_building_is_not_considered(self) -> None:
        # GIVEN
        city = CityFactory()
        older_building = BuildingFactory(city=city, is_published=True)
        BuildingFactory(city=city, is_published=False)

        # WHEN
        url = f"/api/v1/twitter/get_building_details/"
        response = self.client.get(url)

        # THEN the actual latest building schould be ignored
        self.assertEqual(200, response.status_code)
        building_data = response.json().get("data")
        self.assertEqual(building_data.get("id"), older_building.id)

    def test_no_unpublished_on_twitter_buildings_exist(self) -> None:
        # GIVEN
        city = CityFactory()
        BuildingFactory(
            city=city,
            is_published=True,
            published_on_twitter=timezone.now() - timezone.timedelta(days=2),
        )
        BuildingFactory(
            city=city,
            is_published=True,
            published_on_twitter=timezone.now() - timezone.timedelta(days=1),
        )

        # WHEN
        url = f"/api/v1/twitter/get_building_details/"
        response = self.client.get(url)

        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json().get("error").get("message"), "Buildings do not exist."
        )

    def test_multiple_architects_are_merged(self) -> None:
        # GIVEN
        city = CityFactory()
        architect_a = ArchitectFactory(is_published=True)
        architect_b = ArchitectFactory(is_published=True)
        building = BuildingFactory(city=city, is_published=True)
        building.architects.add(architect_a, architect_b)

        # WHEN
        url = f"/api/v1/twitter/get_building_details/"
        response = self.client.get(url)

        # THEN
        self.assertEqual(response.status_code, 200)
        building_data = response.json().get("data")
        self.assertEqual(
            building_data.get("architect"), f"{architect_a.last_name} et al."
        )

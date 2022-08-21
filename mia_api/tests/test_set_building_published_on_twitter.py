from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from mia_buildings.models import Building
from mia_buildings.tests.factories import BuildingFactory
from django.test.utils import ignore_warnings

ignore_warnings(message="No directory at", module="whitenoise.base").enable()


class TwitterBuildingAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            "admin", "admin@example.com", "admin123"
        )
        self.client.force_authenticate(user=self.user)

    def test_update_building_204(self) -> None:
        # GIVEN
        building = BuildingFactory()

        # WHEN
        url = f"/api/v1/twitter/{building.pk}/published_on_twitter/"
        response = self.client.patch(url)

        # THEN
        self.assertEqual(response.status_code, 204)
        building = Building.objects.get(pk=building.pk)
        self.assertTrue(building.published_on_twitter is not None)

    def test_building_does_not_exist(self) -> None:
        # WHEN
        url = f"/api/v1/twitter/1/published_on_twitter/"
        response = self.client.patch(url)

        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json().get("error").get("message"), "Building does not exist"
        )

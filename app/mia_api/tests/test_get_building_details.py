from django.contrib.auth.models import User
from django.test import TestCase
from mia_buildings.tests.factories import BuildingFactory
from mia_facts.tests.factories import CityFactory
from rest_framework.authtoken.models import Token


class BuildingAPITestCase(TestCase):
    def test_get_building_returns_401_unauthorized_if_called_without_token(
        self,
    ) -> None:
        # GIVEN
        building = BuildingFactory(is_published=True, city=CityFactory())

        # WHEN
        url = f"/api/v1/buildings/{building.pk}/"
        response = self.client.get(url)

        # THEN
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_text, "Unauthorized")

    def test_get_building_returns_200_if_called_with_token(self) -> None:
        # GIVEN
        building = BuildingFactory(is_published=True, city=CityFactory())
        user = User.objects.create(username="testuser", password="testpassword")
        token = Token.objects.create(user=user)

        # WHEN
        url = f"/api/v1/buildings/{building.id}/"
        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        response = self.client.get(url, **headers)

        # THEN
        self.assertEqual(response.status_code, 200)

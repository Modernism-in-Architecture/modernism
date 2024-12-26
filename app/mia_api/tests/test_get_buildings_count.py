from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from mia_buildings.tests.factories import BuildingFactory
from rest_framework.authtoken.models import Token


class BuildingsCountAPITestCase(TestCase):
    def test_get_buildings_count_returns_401_unauthorized_if_called_without_token(
        self,
    ) -> None:
        # ACT
        url = "/api/v1/buildings/count/"
        response = self.client.get(url)

        # ASSERT
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_text, "Unauthorized")

    def test_get_buildings_count_returns_200_if_called_with_token(
        self,
    ) -> None:
        # PREPARE
        user = User.objects.create(username="testuser", password="testpassword")
        token = Token.objects.create(user=user)

        # ACT
        url = "/api/v1/buildings/count/"
        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        response = self.client.get(url, **headers)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 0)

    def test_get_buildings_count_counts_only_published_buildings(
        self,
    ) -> None:
        # PREPARE
        user = User.objects.create(username="testuser", password="testpassword")
        token = Token.objects.create(user=user)
        BuildingFactory(is_published=False)

        # ACT
        url = "/api/v1/buildings/count/"
        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        response = self.client.get(url, **headers)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 0)

        # ACT
        BuildingFactory(is_published=True)
        url = "/api/v1/buildings/count/"
        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        response = self.client.get(url, **headers)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)

    def test_get_buildings_count_filters_by_date(
        self,
    ) -> None:
        # PREPARE
        user = User.objects.create(username="testuser", password="testpassword")
        token = Token.objects.create(user=user)
        BuildingFactory(is_published=True)

        # ACT
        url = "/api/v1/buildings/count/?since=2024-12-25T22:34:26.365+01:00"
        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        response = self.client.get(url, **headers)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)

        # PREPARE request one day later
        building = BuildingFactory(is_published=True)
        created_date = building.created
        one_day_later = created_date + timedelta(days=1)
        request_date_format = one_day_later.isoformat()

        # ACT
        url = f"/api/v1/buildings/count/?since={request_date_format}"
        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        response = self.client.get(url, **headers)

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 0)

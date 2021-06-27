import json

import requests
from buildings.tests import factories
from django.test import Client, LiveServerTestCase, TestCase
from wagtail.core.models import Page, Site


class TestPageModels(LiveServerTestCase):
    @classmethod
    def setUp(cls):
        cls.site = Site.objects.create(
            is_default_site=True, root_page=Page.get_first_root_node()
        )
        cls.homepage = factories.HomePageFactory()

        cls.peopleindexpage = factories.PersonsIndexPageFactory(parent=cls.homepage)
        cls.buildingindexpage = factories.BuildingsIndexPageFactory(parent=cls.homepage)

        cls.architectsindexpage = factories.ArchitectsIndexPageFactory(
            parent=cls.peopleindexpage
        )
        cls.developersindexpage = factories.DevelopersIndexPageFactory(
            parent=cls.peopleindexpage
        )

        cls.developerpage = factories.DeveloperPageFactory(
            parent=cls.developersindexpage
        )
        cls.architectpage_1 = factories.ArchitectPageFactory(
            parent=cls.architectsindexpage
        )
        cls.architectpage_2 = factories.ArchitectPageFactory(
            parent=cls.architectsindexpage
        )

        cls.country_1 = factories.CountryFactory()
        cls.country_2 = factories.CountryFactory()
        cls.city_1 = factories.CityFactory(country=cls.country_1)
        cls.city_2 = factories.CityFactory(country=cls.country_1)
        cls.city_3 = factories.CityFactory(country=cls.country_2)

        cls.construction_type_1 = factories.ConstructionTypeFactory()
        cls.building_type_1 = factories.BuildingTypeFactory()
        cls.access_type_1 = factories.AccessTypeFactory()
        cls.position_1 = factories.PositionFactory()
        cls.position_2 = factories.PositionFactory()
        cls.details_1 = factories.DetailFactory()
        cls.details_2 = factories.DetailFactory()
        cls.details_3 = factories.DetailFactory()
        cls.window_1 = factories.WindowFactory()
        cls.roof_1 = factories.RoofFactory()
        cls.roof_2 = factories.RoofFactory()
        cls.facade_1 = factories.FacadeFactory()

        # Building 1
        cls.buildingpage_1 = factories.BuildingPageFactory(
            parent=cls.buildingindexpage,
            city=cls.city_1,
            country=cls.country,
            construction_types=[cls.construction_type_1],
            building_type=cls.building_type_1,
            access_type=cls.access_type_1,
            positions=[cls.position_1, cls.position_2],
            details=[cls.details_1, cls.details_2, cls.details_3],
            windows=[cls.window_1],
            roofs=[cls.roof_1, cls.roof_2],
            facades=[cls.facade_1],
        )

        cls.b_a_relation_1 = factories.BuildingPageArchitectRelationFactory(
            page=cls.buildingpage, architect=cls.architectpage_1
        )
        cls.b_a_relation_2 = factories.BuildingPageArchitectRelationFactory(
            page=cls.buildingpage, architect=cls.architectpage_2
        )
        cls.b_d_relation_1 = factories.BuildingPageDeveloperRelationFactory(
            page=cls.buildingpage, developer=cls.developerpage
        )

        # Building 2
        cls.buildingpage_2 = factories.BuildingPageFactory(
            parent=cls.buildingindexpage,
            city=cls.city_2,
            country=cls.country_1,
            construction_types=[cls.construction_type_1],
            building_type=cls.building_type_1,
            access_type=cls.access_type_1,
            positions=[cls.position_1, cls.position_2],
            details=[cls.details_1, cls.details_2, cls.details_3],
            windows=[cls.window_1],
            roofs=[cls.roof_1, cls.roof_2],
            facades=[cls.facade_1],
        )

        cls.b_a_relation_2 = factories.BuildingPageArchitectRelationFactory(
            page=cls.buildingpage, architect=cls.architectpage_2
        )
        cls.b_d_relation_1 = factories.BuildingPageDeveloperRelationFactory(
            page=cls.buildingpage, developer=cls.developerpage
        )

    def test_setup(self):
        self.maxDiff = None

        # WHEN
        c = Client()
        response = c.post(
            f"{self.buildingindexpage.url_path}",
            {"username": "john", "password": "smith"},
        )

        # THEN
        self.assertEqual(response.status_code, 200)


from buildings.tests import factories
from django.test import TestCase
from wagtail.core.models import Page, Site


class TestPageModels(TestCase):
    @classmethod
    def setUpTestData(cls):
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

        cls.country = factories.CountryFactory()
        cls.city_1 = factories.CityFactory(country=cls.country)
        cls.city_2 = factories.CityFactory(country=cls.country)

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

        cls.buildingpage = factories.BuildingPageFactory(
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

    def test_setup(self):
        pass


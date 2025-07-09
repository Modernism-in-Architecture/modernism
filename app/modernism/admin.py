from django.contrib.admin import AdminSite
from mia_buildings.models import Building, BuildingImage
from mia_people.models import Architect


class MiaAdminSite(AdminSite):
    site_header = "MIA Admin"
    site_title = "MIA Admin"
    index_title = "MIA Dashboard"

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        extra_context["dashboard_data"] = {
            "architects": {
                "published": Architect.objects.filter(is_published=True).count(),
                "unpublished": Architect.objects.filter(is_published=False).count(),
            },
            "buildings": {
                "published": Building.objects.filter(is_published=True).count(),
                "unpublished": Building.objects.filter(is_published=False).count(),
            },
            "images": {
                "published": BuildingImage.objects.filter(is_published=True).count(),
                "unpublished": BuildingImage.objects.filter(is_published=False).count(),
            }
        }

        return super().index(request, extra_context=extra_context)
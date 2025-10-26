from collections import defaultdict
from datetime import datetime

from django.contrib.admin import AdminSite
from mia_buildings.models import Building, BuildingImage
from mia_general.models import ToDoItem
from mia_people.models import Architect


class MiaAdminSite(AdminSite):
    site_header = "MIA Admin"
    site_title = "MIA Admin"
    index_title = "Dashboard"

    def get_grouped_todo_items(self):
        grouped = defaultdict(
            lambda: {
                "count": 0,
                "cities": defaultdict(lambda: {"count": 0, "items": []}),
            }
        )

        todos = (
            ToDoItem.objects.select_related("city__country")
            .prefetch_related("buildingimage_set")
            .filter(is_completed=False)
        )

        for todo in todos:
            country_name = (
                todo.city.country.name
                if todo.city and todo.city.country
                else "Unknown Country"
            )
            city_name = todo.city.name if todo.city else "Unknown City"

            grouped[country_name]["count"] += 1
            grouped[country_name]["cities"][city_name]["count"] += 1
            grouped[country_name]["cities"][city_name]["items"].append(todo)

        result = {
            country: {
                "count": data["count"],
                "cities": dict(data["cities"]),
            }
            for country, data in grouped.items()
        }

        return result, todos.count()

    def each_context(self, request):
        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        context = super().each_context(request)

        grouped_todo_items, todos_count = self.get_grouped_todo_items()

        context["custom_index_title"] = f"{greeting} 👋"
        context["custom_index_date"] = f"{now.strftime('%-d %B %Y')}"
        context["todos_count"] = todos_count
        context["grouped_todo_items"] = grouped_todo_items

        return context

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
                "unrelated": BuildingImage.objects.filter(
                    building__isnull=True, todo_item__isnull=True, is_archived=False
                ).count(),
                "todos": BuildingImage.objects.filter(
                    building__isnull=True, todo_item__isnull=False
                ).count(),
                "archived": BuildingImage.objects.filter(is_archived=True).count(),
            },
        }

        return super().index(request, extra_context=extra_context)

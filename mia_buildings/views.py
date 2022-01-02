from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.serializers import serialize
from django.db.models.query import Prefetch
from django.http.request import MultiValueDict, QueryDict
from django.shortcuts import redirect, render
from el_pagination.decorators import page_template
from mia_facts.models import Fact, Photographer
from rest_framework.decorators import api_view

from mia_buildings.forms import BuildingsFilterForm, BulkUploadImagesForm
from mia_buildings.models import Building, BuildingImage


def _get_filtered_buildings(cleaned_form_data, buildings):
    architects = cleaned_form_data.get("architects")
    if architects.exists():
        buildings = buildings.filter(
            architects__id__in=architects.values_list("id", flat=True)
        )
        if not buildings:
            return buildings.none()

    developers = cleaned_form_data.get("developers")
    if developers.exists():
        buildings = buildings.filter(
            developers__id__in=developers.values_list("id", flat=True)
        )
        if not buildings:
            return buildings.none()

    countries = cleaned_form_data.get("countries")
    if countries.exists():
        buildings = buildings.filter(
            city__country__name__in=countries.values_list("name", flat=True)
        )
        if not buildings:
            return buildings.none()

    cities = cleaned_form_data.get("cities")
    if cities.exists():
        buildings = buildings.filter(city_id__in=cities.values_list("id", flat=True))
        if not buildings:
            return buildings.none()

    positions = cleaned_form_data.get("positions")
    if positions.exists():
        buildings = buildings.filter(
            positions__id__in=positions.values_list("id", flat=True)
        ).distinct()
        if not buildings:
            return buildings.none()

    details = cleaned_form_data.get("details")
    if details.exists():
        buildings = buildings.filter(
            details__id__in=details.values_list("id", flat=True).distinct()
        )
        if not buildings:
            return buildings.none()

    windows = cleaned_form_data.get("windows")
    if windows.exists():
        buildings = buildings.filter(
            windows__id__in=windows.values_list("id", flat=True).distinct()
        )
    roofs = cleaned_form_data.get("roofs")
    if roofs.exists():
        buildings = buildings.filter(
            roofs__id__in=roofs.values_list("id", flat=True).distinct()
        )
        if not buildings:
            return buildings.none()

    facades = cleaned_form_data.get("facades")
    if facades.exists():
        buildings = buildings.filter(
            facades__id__in=facades.values_list("id", flat=True).distinct()
        )
        if not buildings:
            return buildings.none()

    construction_types = cleaned_form_data.get("construction_types")
    if construction_types.exists():
        buildings = buildings.filter(
            construction_types__id__in=construction_types.values_list(
                "id", flat=True
            ).distinct()
        )
        if not buildings:
            return buildings.none()

    years = cleaned_form_data.get("years")
    if years:
        buildings = buildings.filter(year_of_construction__in=years)
        if not buildings:
            return buildings.none()

    building_type = cleaned_form_data.get("building_types")
    if building_type:
        buildings = buildings.filter(building_type=building_type)
        if not buildings:
            return buildings.none()

    access_type = cleaned_form_data.get("access_type")
    if access_type:
        buildings = buildings.filter(access_type=access_type)
        if not buildings:
            return buildings.none()

    is_protected_monument = cleaned_form_data.get("protected_monument")
    if is_protected_monument != "":
        buildings = buildings.filter(protected_monument=is_protected_monument)
        if not buildings:
            return buildings.none()

    storey = cleaned_form_data.get("storey")
    if storey != "":
        buildings = buildings.filter(storey=storey)
        if not buildings:
            return buildings.none()

    return buildings.distinct()


@page_template("mia_buildings/building_list.html")
def get_building_list(
    request, template="mia_buildings/building_index.html", extra_context=None
):
    building_list = (
        Building.objects.filter(is_published=True)
        .select_related("city__country")
        .prefetch_related(
            Prefetch(
                "buildingimage_set",
                queryset=BuildingImage.objects.filter(
                    is_published=True, is_feed_image=True
                ),
                to_attr="feed_images",
            )
        )
        .order_by("-created")
    )
    context = {}
    search_query = request.GET.get("q", None)

    if request.method == "POST":

        building_form = BuildingsFilterForm(request.POST)
        request.session["filter-request"] = dict(request.POST)

        if building_form.is_valid():

            context["form"] = building_form
            building_list = _get_filtered_buildings(
                building_form.cleaned_data, building_list
            )

    else:
        current_filter_settings = request.session.get("filter-request")
        context["form"] = BuildingsFilterForm()

        if current_filter_settings is not None:
            for setting, value in list(current_filter_settings.items()):
                try:
                    if value[0] == "":
                        del current_filter_settings[setting]
                except KeyError:
                    continue

            filter_query_dict = QueryDict("", mutable=True)
            filter_query_dict.update(MultiValueDict(current_filter_settings))
            building_form = BuildingsFilterForm(filter_query_dict)

            if building_form.is_valid():
                context["form"] = building_form
                building_list = _get_filtered_buildings(
                    building_form.cleaned_data, building_list
                )

    if search_query:
        building_list = (
            building_list.annotate(
                search=SearchVector(
                    "name",
                    "history",
                    "subtitle",
                    "description",
                    "architects__last_name",
                    "developers__last_name",
                    "city__country__name",
                    "city__name",
                ),
            )
            .filter(search=search_query)
            .distinct("created")
        )
    context["buildings"] = building_list
    context["search_term"] = search_query

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_building_details(
    request,
    slug,
    template="mia_buildings/building_details.html",
    extra_context=None,
):

    building = (
        Building.objects.filter(is_published=True, slug=slug)
        .select_related("city")
        .select_related("access_type")
        .prefetch_related("architects")
        .prefetch_related("developers")
        .prefetch_related("building_types")
        .prefetch_related("positions")
        .prefetch_related("details")
        .prefetch_related("windows")
        .prefetch_related("roofs")
        .prefetch_related("facades")
        .prefetch_related("construction_types")
        .prefetch_related("sources")
        .prefetch_related(
            Prefetch(
                "buildingimage_set",
                queryset=BuildingImage.objects.filter(is_published=True),
                to_attr="gallery_images",
            )
        )
        .prefetch_related(
            Prefetch(
                "buildingimage_set",
                queryset=BuildingImage.objects.filter(
                    is_published=True, is_feed_image=True
                ),
                to_attr="feed_images",
            )
        )
        .first()
    )

    buildings_of_same_city = Building.objects.filter(
        is_published=True, city=building.city
    )

    city_fact = Fact.objects.filter(title=building.city).first()
    country_fact = Fact.objects.filter(title=building.city.country).first()

    context = {
        "building": building,
        "buildings_of_same_city": serialize(
            "json",
            buildings_of_same_city,
            fields=("pk", "latitude", "longitude", "slug", "name", "address"),
        ),
        "city_fact": city_fact,
        "country_fact": country_fact,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@login_required(login_url="/admin/login/")
def bulkupload_images(request):
    if request.method == "POST":
        form = BulkUploadImagesForm(request.POST, request.FILES)

        if form.is_valid():

            images = request.FILES.getlist("multiple_images")
            building_photographer = None
            photographer_id = form.cleaned_data.get("photographer")
            title = form.cleaned_data.get("title")
            tags = form.cleaned_data.get("tags")

            if photographer_id:
                building_photographer = Photographer.objects.filter(
                    id=photographer_id
                ).first()

            for index, image in enumerate(images):
                building_image = BuildingImage.objects.create(image=image)
                building_image.title = f"{title} - {index}"
                building_image.photographer = building_photographer
                if tags:
                    building_image.tags.add(*tags)
                building_image.save()

            messages.success(
                request,
                f"Upload of {len(images)} pics finished successfully. We love new images for MIA <3",
            )

            return redirect(
                "admin:mia_buildings_buildingimage_changelist",
            )

    form = BulkUploadImagesForm()
    payload = {"form": form, "title": "Upload multiple images"}

    return render(request, "admin/bulkupload_images.html", payload)

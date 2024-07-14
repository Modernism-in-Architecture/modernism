from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mia_facts.models import Photographer

from mia_buildings.admin_forms import BulkUploadImagesForm
from mia_buildings.models import BuildingImage


@login_required(login_url="/admin/login/")
def bulkupload_images(request):
    if request.method == "POST":
        form = BulkUploadImagesForm(request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist("multiple_images")
            building_photographer = None
            photographer_id = form.cleaned_data.get("photographer")
            title = form.cleaned_data.get("title")

            if photographer_id:
                building_photographer = Photographer.objects.filter(
                    id=photographer_id
                ).first()

            for index, image in enumerate(images):
                building_image = BuildingImage.objects.create(image=image)
                building_image.title = f"{title} - {index}"
                building_image.photographer = building_photographer
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

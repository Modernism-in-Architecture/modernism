from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mia_general.models import ToDoItem

from mia_buildings.admin_forms import BulkUploadImagesForm
from mia_buildings.models import BuildingImage


@login_required(login_url="/admin/login/")
def bulkupload_images(request):
    if request.method == "POST":
        form = BulkUploadImagesForm(request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist("multiple_images")
            photographer = form.cleaned_data.get("photographer")
            name_for_images = form.cleaned_data.get("name_for_images")
            notes = form.cleaned_data["notes"]
            title = form.cleaned_data["building_working_title"]
            city = form.cleaned_data["city"]
            selected_todo = form.cleaned_data.get("todo_item")

            if selected_todo:
                todo_item = selected_todo
            else:
                todo_item = ToDoItem.objects.create(title=title, city=city, notes=notes)

            building_images = []
            for index, image in enumerate(images):
                building_image = BuildingImage(
                    image=image,
                    title=f"{name_for_images} - {index}",
                    photographer=photographer,
                    todo_item=todo_item,
                )
                building_images.append(building_image)

            BuildingImage.objects.bulk_create(building_images)

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

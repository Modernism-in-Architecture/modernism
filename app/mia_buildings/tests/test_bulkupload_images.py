import io
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import override_settings
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse
from mia_facts.models import City, Photographer
from mia_general.models import ToDoItem
from PIL import Image

from mia_buildings.models import BuildingImage


def generate_test_image_file(name="test.jpg"):
    img = Image.new("RGB", (100, 100), color="blue")
    file = io.BytesIO()
    file.name = name
    img.save(file, "JPEG")
    file.seek(0)
    return file


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username="admin", password="adminpass", is_staff=True
    )


@pytest.fixture
def logged_in_client(client, staff_user):
    client.login(username="admin", password="adminpass")
    return client


@pytest.mark.django_db
@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.InMemoryStorage",
        }
    }
)
@patch("mia_buildings.models.BuildingImage.image.field.storage.save")
def test_bulk_upload_creates_todoitem_and_assigns_images(mock_save, logged_in_client):
    mock_save.side_effect = lambda name, content, **kwargs: name

    url = reverse("admin:bulkupload-images")

    city = City.objects.create(name="Graz")
    photographer = Photographer.objects.create(last_name="Doe")

    image1 = generate_test_image_file("img1.jpg")
    image2 = generate_test_image_file("img2.jpg")

    post_data = {
        "building_working_title": "Test Building",
        "name_for_images": "Test Images",
        "notes": "Notes",
        "city": str(city.id),
        "photographer": str(photographer.id),
    }

    file_data = {
        "multiple_images": [image1, image2],
    }

    response = logged_in_client.post(
        url,
        data={**post_data, **file_data},
        content_type=MULTIPART_CONTENT,
    )

    assert response.status_code == 302

    todos = ToDoItem.objects.filter(title="Test Building")
    assert todos.count() == 1
    todo = todos.first()
    todo.city = city
    todo.title = "Test Building"
    todo.notes = "Notes"

    images = BuildingImage.objects.filter(todo_item=todo)

    assert images.count() == 2
    assert all(img.photographer == photographer for img in images)
    assert all(img.title.startswith("Test Images") for img in images)
    assert all(img.todo_item == todo for img in images)

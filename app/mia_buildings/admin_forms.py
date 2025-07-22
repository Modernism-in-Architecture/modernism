from django.forms import (
    CharField,
    ClearableFileInput,
    Form,
    ImageField,
    ModelChoiceField,
    ModelForm,
    Select,
    Textarea,
    ValidationError,
)
from django.forms.widgets import MultipleHiddenInput
from mia_facts.models import City, Photographer
from mia_general.models import ToDoItem
from modernism.mixins import ContentMarkupMixin
from tinymce.widgets import TinyMCE

from mia_buildings.models import Building


class MultipleImageFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageFileField(ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, list | tuple):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class BulkUploadImagesForm(Form):
    building_working_title = CharField(label="Working title for the building", help_text="Title is only used for the TODO item,  not the building itself", widget=Textarea(attrs={"rows": "1"}))
    city = ModelChoiceField(
        queryset=City.objects.order_by("name"),
        widget=Select(attrs={"class": "select2-field"})
    )
    name_for_images = CharField(label="General name for the images", widget=Textarea(attrs={"rows": "1"}))
    photographer= ModelChoiceField(
        queryset=Photographer.objects.all().order_by("last_name"),
        required=False,
        widget=Select(attrs={"class": "select2-field"})
    )
    todo_item = ModelChoiceField(
        help_text="Create a new or select an existing ToDo item",
        queryset=ToDoItem.objects.filter(is_completed=False).order_by("-created"),
        required=False,
        empty_label="(Create new ToDo)",
        widget=Select(attrs={"class": "select2-field"})
    )
    notes = CharField(label="Further notes", required=False, widget=Textarea(attrs={"rows": "2"}))
    multiple_images = MultipleImageFileField(label="Select images")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BuildingAdminForm(ContentMarkupMixin, ModelForm):
    class Meta:
        model = Building
        widgets = {
            "subtitle": Textarea(attrs={"rows": "2"}),
            "seo_title": Textarea(attrs={"rows": "2"}),
            "history": TinyMCE(
                mce_attrs={"convert_urls": False, "browser_spellcheck": True}
            ),
            "description": TinyMCE(
                mce_attrs={"convert_urls": False, "browser_spellcheck": True}
            ),
            "directions": Textarea(attrs={"rows": "3"}),
            "address": Textarea(attrs={"rows": "3"}),
        }
        fields = "__all__"


class BuildingForImageSelectionAdminForm(Form):
    _selected_action = CharField(widget=MultipleHiddenInput)
    _images = CharField(widget=MultipleHiddenInput)
    building = ModelChoiceField(
        queryset=Building.objects.all().order_by("name"),
        widget=Select,
    )

class AssignOrCreateToDoItemForm(Form):
    _selected_action = CharField(widget=MultipleHiddenInput)
    _images = CharField(widget=MultipleHiddenInput)

    todo_item = ModelChoiceField(
        queryset=ToDoItem.objects.filter(is_completed=False).order_by("-created"),
        required=False,
        label="Select existing ToDoItem",
        widget=Select(attrs={"class": "select2"})
    )
    working_title = CharField(label="Working Title", required=False, widget=Textarea(attrs={"rows": "2"}))
    city = ModelChoiceField(
        queryset=City.objects.order_by("name"),
        required=False,
        label="City",
        widget=Select(attrs={"class": "select2"})
    )
    notes = CharField(label="Notes", required=False,  widget=Textarea(attrs={"rows": "2"}))

    def clean(self):
        cleaned = super().clean()
        todo = cleaned.get("todo_item")
        working_title = cleaned.get("working_title")
        city = cleaned.get("city")

        if not todo and not (working_title and city):
            raise ValidationError(
                "Either select an existing ToDoItem or enter a title and city to create one."
            )
        return cleaned
  
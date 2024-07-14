from django.forms import (
    CharField,
    ChoiceField,
    ClearableFileInput,
    Form,
    ImageField,
    ModelChoiceField,
    ModelForm,
    Select,
    Textarea,
)
from django.forms.widgets import MultipleHiddenInput
from mia_facts.models import Photographer
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
    multiple_images = MultipleImageFileField(label="Select images")
    photographer = ChoiceField(required=False, widget=Select, choices=[])
    title = CharField(label="General name for the images")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_photographer_choices()

    def set_photographer_choices(self):
        photographers = Photographer.objects.values_list("id", "last_name").order_by(
            "last_name"
        )
        choices = [(None, "------")] + list(photographers)
        self.fields["photographer"].choices = choices


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

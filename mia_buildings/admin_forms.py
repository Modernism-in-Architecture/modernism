from taggit.models import Tag
from tinymce.widgets import TinyMCE

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import (
    CharField,
    ChoiceField,
    ClearableFileInput,
    Form,
    ImageField,
    ModelChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
    Select,
    Textarea,
)
from django.forms.widgets import MultipleHiddenInput

from mia_buildings.admin_utils import validate_and_clean_content_markup
from mia_buildings.models import Building
from mia_facts.models import Photographer


class MultipleImageFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageFileField(ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class BulkUploadImagesForm(Form):
    multiple_images = MultipleImageFileField(label="Select images")
    photographer = ChoiceField(required=False, widget=Select, choices=[])
    tags = ModelMultipleChoiceField(
        required=False,
        queryset=Tag.objects.order_by("name"),
        widget=FilteredSelectMultiple("Tags", True),
    )
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


class BuildingAdminForm(ModelForm):
    multiple_images = MultipleImageFileField(required=False)
    photographer = ChoiceField(
        required=False,
        widget=Select,
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_photographer_choices()

    def set_photographer_choices(self):
        photographers = Photographer.objects.values_list("id", "last_name").order_by(
            "last_name"
        )
        choices = [("", "------")] + list(photographers)
        self.fields["photographer"].choices = choices

    def clean_description(self):
        description = self.cleaned_data.get("description")
        was_clean, cleaned_content_data = validate_and_clean_content_markup(description)

        if not was_clean:
            # Solved in this unconventional way to provide the cleaned data to the user for review
            copied_form_data = self.data.copy()
            copied_form_data["description"] = cleaned_content_data
            self.data = copied_form_data
            raise ValidationError(
                f"Your text markup needed to be cleaned. Please review, correct if necessary and save again."
            )

        return description

    def clean_history(self):
        history_content = self.cleaned_data.get("history")
        clean, cleaned_content_data = validate_and_clean_content_markup(history_content)

        if not clean:
            # Solved in this unconventional way to provide the cleaned data to the user for review
            copied_form_data = self.data.copy()
            copied_form_data["history"] = cleaned_content_data
            self.data = copied_form_data
            raise ValidationError(
                f"Your text markup needed to be cleaned. Please review, correct if necessary and save again."
            )

        return history_content


class BuildingForImageSelectionAdminForm(Form):
    _selected_action = CharField(widget=MultipleHiddenInput)
    _images = CharField(widget=MultipleHiddenInput)
    building = ModelChoiceField(
        queryset=Building.objects.all().order_by("name"),
        widget=Select(),
    )

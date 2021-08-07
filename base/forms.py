from django import forms
from django.utils.text import slugify
from wagtail.admin.forms import WagtailAdminPageForm


class GeneralAdminModelForm(WagtailAdminPageForm):

    slug = forms.SlugField(
        required=False, disabled=True, help_text="Slug is auto-generated."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.initial["slug"]:
            self.initial["slug"] = "auto-generated-slug"

    def save(self, commit=True):
        page = super().save(commit=False)

        last_name = self.cleaned_data.get("last_name", "")
        first_name = self.cleaned_data.get("first_name", "")
        title = self.cleaned_data.get("title", "")
        name = self.cleaned_data.get("name", "")

        if last_name:  # PeoplePage
            slug = last_name
            page.title = slug
            if first_name:
                slug = f"{first_name} {last_name}"
                page.title = slug
        if name:  # BuildingPage
            slug = name
            page.title = slug
        if title:  # FactsPage
            slug = title

        page.slug = slugify(slug)

        if commit:
            page.save()
        return page

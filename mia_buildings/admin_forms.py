from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm

# from mia_buildings.admin_utils import AdminUtils
from mia_buildings.models import Building

#
# class BuildingForm(ModelForm):  # noqa: DJ06
#     class Meta:
#         model = Building
#         exclude = []
#
#     def clean_description(self):
#         description = self.cleaned_data.get("description")
#
#         success, msg = AdminUtils.validate_html(description)
#         if not success:
#             raise ValidationError(f"{msg}")
#         return self.cleaned_data.get("description")
#
#
# class BuildingFormSet(BaseInlineFormSet):
#     def clean(self):
#         super(BuildingFormSet, self).clean()
#
#         for form in self.forms:
#             if not form.is_valid():
#                 return
#             if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
#                 description = form.cleaned_data["description"]
#                 success, msg = AdminUtils.validate_html(description)
#                 if not success:
#                     raise ValidationError(f"{msg}")

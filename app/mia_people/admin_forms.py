from django.forms import ModelForm
from modernism.mixins import ContentMarkupMixin

from mia_people.models import Architect, Developer, Professor


class DeveloperAdminForm(ContentMarkupMixin, ModelForm):
    class Meta:
        model = Developer
        fields = "__all__"


class ArchitectAdminForm(ContentMarkupMixin, ModelForm):
    class Meta:
        model = Architect
        fields = "__all__"


class ProfessorAdminForm(ContentMarkupMixin, ModelForm):
    class Meta:
        model = Professor
        fields = "__all__"

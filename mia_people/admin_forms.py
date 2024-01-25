from django.forms import ModelForm

from mia_people.models import Architect, Developer, Professor
from modernism.mixins import ContentMarkupMixin


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

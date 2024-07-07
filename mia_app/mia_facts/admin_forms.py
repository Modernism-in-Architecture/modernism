from django.forms import ModelForm
from modernism.mixins import ContentMarkupMixin

from mia_facts.models import Fact


class FactAdminForm(ContentMarkupMixin, ModelForm):
    class Meta:
        model = Fact
        fields = "__all__"

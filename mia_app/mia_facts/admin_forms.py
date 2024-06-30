from django.forms import ModelForm

from mia_facts.models import Fact
from modernism.mixins import ContentMarkupMixin


class FactAdminForm(ContentMarkupMixin, ModelForm):
    class Meta:
        model = Fact
        fields = "__all__"

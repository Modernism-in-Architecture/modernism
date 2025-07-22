from django.db import models
from mia_facts.models import City
from modernism.models import BaseModel


class ToDoItem(BaseModel):
    title = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "mia_general"
        verbose_name = "To-Do Item"
        verbose_name_plural = "To-Do Items"

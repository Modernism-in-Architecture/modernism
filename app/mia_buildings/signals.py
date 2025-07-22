import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from mia_general.models import ToDoItem
from modernism.tools import generate_thumbnails_for_image

from mia_buildings.models import Building, BuildingImage

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BuildingImage)
def generate_thumbnails(sender, instance, created, **kwargs):
    if instance.is_published and not instance.thumbnails_created:
        generate_thumbnails_for_image(instance.image, instance.is_feed_image)

        logger.info(
            f"Generated thumbnails for: {instance.title if instance.title else {instance.pk}}"
        )

        instance.thumbnails_created = timezone.now()
        instance.save()


@receiver(pre_save, sender=Building)
def cache_building_published_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_version = sender.objects.get(pk=instance.pk)
            instance._was_published = old_version.is_published
        except sender.DoesNotExist:
           instance._was_published = None


@receiver(post_save, sender=Building)
def complete_todos_on_publish(sender, instance, created, **kwargs):
    was_published = getattr(instance, "_was_published", None)

    if instance.is_published and (created or was_published is False):
        images = instance.buildingimage_set.select_related('todo_item')
        todo_ids = [img.todo_item.id for img in images if img.todo_item]
        if todo_ids:
            ToDoItem.objects.filter(id__in=todo_ids).update(is_completed=True)

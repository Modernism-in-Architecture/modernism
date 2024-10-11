import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from modernism.tools import generate_thumbnails_for_image

from mia_buildings.models import BuildingImage

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

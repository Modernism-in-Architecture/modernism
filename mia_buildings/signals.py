import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from mia_buildings.models import Building
from modernism.tools import generate_thumbnails_for_image


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Building)
def generate_thumbnails(sender, instance, created, **kwargs):
    if instance.is_published:
        if not instance.thumbnails_created and instance.buildingimage_set.exists():
            images = instance.buildingimage_set.filter(is_published=True)

            for image in images:
                generate_thumbnails_for_image(image.image, image.is_feed_image)

            logger.info(f"Generating thumbnails for: {instance.name}")

            instance.thumbnails_created = timezone.now()
            instance.save()

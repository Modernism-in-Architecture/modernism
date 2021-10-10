from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmetadata.models import MetadataPageMixin


def get_image_model_string():
    try:
        image_model = settings.WAGTAILIMAGES_IMAGE_MODEL
    except AttributeError:
        image_model = "wagtailimages.Image"
    return image_model


class CustomMetadataPageMixin(MetadataPageMixin):
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=ugettext_lazy("Search image"),
    )

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("search_description"),
                ImageChooserPanel("search_image"),
            ],
            ugettext_lazy("Common page configuration"),
        ),
    ]

    def get_meta_title(self):
        """The title of this object"""
        return self.seo_title or self.title

    def get_meta_url(self):
        """The URL of this object, including protocol and domain"""
        return self.full_url

    def get_meta_description(self):
        """
        A short text description of this object.
        This should be plain text, not HTML.
        """
        return self.search_description

    def get_meta_image_url(self, request):
        """
        Return a url for an image to use, see the MetadataPageMixin if using a Wagtail image
        """
        return self.search_image.file.url

    def get_meta_twitter_card_type(self):
        """
        What kind of Twitter card to show this as.
        Defaults to ``summary_large_photo`` if there is a meta image,
        or ``summary`` if there is no image. Optional.
        """
        return "summary_large_photo"

    class Meta:
        abstract = True

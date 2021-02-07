from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock


class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "large": value.get_rendition("max-1300x700").attrs_dict,
            }


class GalleryImageBlock(StructBlock):
    image = ImageChooserBlock()
    description = TextBlock(required=False)
    photographer = CharBlock(required=False)

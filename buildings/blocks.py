from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock


class GalleryImageBlock(StructBlock):
    image = ImageChooserBlock()
    description = TextBlock(required=False)
    photographer = CharBlock(required=False)

import logging
import os
from bs4 import BeautifulSoup
from easy_thumbnails.files import get_thumbnailer
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile


logger = logging.getLogger(__name__)


def validate_and_clean_content_markup(html: str) -> tuple[bool, str]:
    soup = BeautifulSoup(html, "html.parser")
    before = str(soup)
    cleanup(soup)
    after = str(soup)
    return before == after, after


def cleanup(document: BeautifulSoup) -> None:
    ATTRIBUTE_WHITELIST = ["href", "src"]
    ELEMENT_WHITELIST = ["p", "a", "em", "strong"]

    def removeAttributes(element):
        for attr in set(element.attrs):
            if attr not in ATTRIBUTE_WHITELIST:
                del element[attr]

    def removeEmptyElement(element):
        if len(element.get_text(strip=True)) == 0:
            element.extract()

    def unwrapElement(element):
        if element.name not in ELEMENT_WHITELIST:
            element.unwrap()

    def cleanupElement(element):
        removeAttributes(element)
        unwrapElement(element)
        removeEmptyElement(element)

    result = document.find_all()
    for entry in result:
        cleanupElement(entry)


def generate_thumbnails_for_image(image: ImageFieldFile, is_feed_image: bool):
    try:
        get_thumbnailer(image)["mobile"].url
        get_thumbnailer(image)["large"].url

        if is_feed_image:
            get_thumbnailer(image)["feed"].url
            get_thumbnailer(image)["preview"].url
            get_thumbnailer(image)["square"].url

    except Exception as e:
        logger.info(f"Error generating thumbnails for image {image.pk}: {str(e)}")


def create_thumbnail_image_path(image: str, thumbnail_type_settings: str) -> str:
    """
    image path ex.: 'original_images/Biel_Volkshaus_General-Guisan-Platz_0.JPG'
    target url ex.: 'https://modernism.s3.amazonaws.com/original_images/thumbs/IMG_1025.jpeg.150x150_q85_crop.jpg'
    """

    host = settings.MEDIA_URL  # f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    subdir = settings.THUMBNAIL_SUBDIR  # "thumbs"
    directory, filename = os.path.split(
        image
    )  # "original_images/Biel_Volkshaus_General-Guisan-Platz_0.JPG"

    thumbnail_url = f"{host}{directory}/{subdir}/{filename}{thumbnail_type_settings}"

    return thumbnail_url

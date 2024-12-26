import logging
import os

from bs4 import BeautifulSoup
from dateutil.parser import parse
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from django.utils.timezone import make_aware, utc
from easy_thumbnails.files import get_thumbnailer

logger = logging.getLogger(__name__)

ATTRIBUTE_WHITELIST = ["href", "src"]
ELEMENT_WHITELIST = ["p", "a", "em", "strong"]


def validate_and_clean_content_markup(html: str) -> tuple[bool, str]:
    soup = BeautifulSoup(html, "html.parser")
    before = str(soup)
    cleanup(soup)
    after = str(soup)
    return before == after, after


def cleanup(document: BeautifulSoup) -> None:
    def remove_attributes(element):
        for attr in set(element.attrs):
            if attr not in ATTRIBUTE_WHITELIST:
                del element[attr]

    def remove_empty_element(element):
        if len(element.get_text(strip=True)) == 0:
            element.extract()

    def unwrap_element(element):
        if element.name not in ELEMENT_WHITELIST:
            element.unwrap()

    def cleanup_element(element):
        remove_attributes(element)
        unwrap_element(element)
        remove_empty_element(element)

    result = document.find_all()
    for entry in result:
        cleanup_element(entry)


def generate_thumbnails_for_image(image: ImageFieldFile, is_feed_image: bool):
    try:
        logger.info(f"Generating thumbnails for image {image}")
        get_thumbnailer(image)["mobile"]
        logger.info(f"Mobile thumbnail generated for {image}")
        get_thumbnailer(image)["large"]
        logger.info(f"Large thumbnail generated for {image}")

        if is_feed_image:
            get_thumbnailer(image)["feed"]
            get_thumbnailer(image)["preview"]
            get_thumbnailer(image)["square"]
            logger.info(f"Feed thumbnails generated for {image}")

    except Exception as e:
        logger.info(f"Error generating thumbnails for image {image}: {str(e)}")


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


def parse_date_with_timezone(date_str):
    try:
        dt = parse(date_str)
        if dt.tzinfo is None:
            from django.utils.timezone import get_default_timezone

            dt = make_aware(dt, get_default_timezone())
        return dt
    except ValueError:
        return None


def normalize_to_utc(dt):
    return dt.astimezone(utc)

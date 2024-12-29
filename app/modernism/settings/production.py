from __future__ import absolute_import, unicode_literals

from .base import *

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"

AWS_STORAGE_BUCKET_NAME = "modernism"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = None

MEDIA_ROOT = ""
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

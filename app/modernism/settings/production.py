from __future__ import absolute_import, unicode_literals

import dj_database_url

from .base import *

env = os.environ.copy()

SECRET_KEY = env["SECRET_KEY"]

DEBUG = False

DATABASES["default"] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [".modernism-in-architecture.org", ".mia-archive.org", ".mia-archiv.de"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"

AWS_STORAGE_BUCKET_NAME = "modernism"
AWS_ACCESS_KEY_ID = env["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = env["AWS_SECRET_ACCESS_KEY"]
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = None

MEDIA_ROOT = ""
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

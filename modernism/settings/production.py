from __future__ import absolute_import, unicode_literals

import os

import dj_database_url

from .base import *

env = os.environ.copy()
SECRET_KEY = env["SECRET_KEY"]

DEBUG = False

DATABASES["default"] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = ["*"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"

try:
    from .local import *
except ImportError:
    pass

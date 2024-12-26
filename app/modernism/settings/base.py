import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    # Third-Party
    "adminsortable2",
    "el_pagination",
    "easy_thumbnails",
    "rest_framework",
    "rest_framework.authtoken",
    "storages",
    "taggit",
    "tinymce",
    # Local
    "mia_buildings",
    "mia_people",
    "mia_facts",
    "mia_general",
    "mia_api",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "modernism.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "modernism.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "modernism",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

THUMBNAIL_SUBDIR = "thumbs"
THUMBNAIL_ALIASES = {
    "": {
        "preview": {"size": (150, 150), "crop": True},
        "feed": {"size": (350, 350), "crop": True},
        "large": {"size": (1300, 700), "crop": False},
        "mobile": {"size": (1200, 0), "quality": 60},
        "square": {"size": (500, 500), "crop": True},
    },
}

THUMBNAIL_PATHS = {  #
    "preview": ".150x150_q85_crop.jpg",  # https://modernism.s3.amazonaws.com/original_images/thumbs/IMG_1025.jpeg.150x150_q85_crop.jpg
    "feed": ".350x350_q85_crop.jpg",  # https://modernism.s3.amazonaws.com/original_images/thumbs/IMG_1025.jpeg.350x350_q85_crop.jpg
    "large": ".1300x700_q85.jpg",  # https://modernism.s3.amazonaws.com/original_images/thumbs/Atrium_3.JPG.1300x700_q85.jpg
    "square": ".500x500_q85_crop.jpg",  # https://modernism.s3.amazonaws.com/original_images/thumbs/Atrium_3.JPG.500x500_q85_crop.jpg
    "mobile": ".1200x0_q60.jpg",  # https://modernism.s3.amazonaws.com/original_images/thumbs/Schunck.jpg.1200x0_q60.jpg
}

BASE_URL = "https://modernism-in-architecture.org"

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "width": "80%",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,charmap,fullscreen,insertdatetime,media,paste,code,wordcount",
    "toolbar": "undo redo | bold italic | link | code",
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"user": "1000/day"},
}

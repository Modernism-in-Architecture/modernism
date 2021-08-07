from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .api import api_router

urlpatterns = [
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/", include(wagtailadmin_urls)),
    # url(r"^jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^api/v2/", api_router.urls),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns


urlpatterns = urlpatterns + [
    url(r"", include(wagtail_urls)),
]

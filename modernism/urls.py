from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from modernism.sitemaps import (
    ArchitectsSitemap,
    BuildingsSitemap,
    DevelopersSitemap,
    FactsSitemap,
    ProfessorsSitemap,
    StaticViewSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "buildings": BuildingsSitemap,
    "architects": ArchitectsSitemap,
    "developers": DevelopersSitemap,
    "professors": ProfessorsSitemap,
    "facts": FactsSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mia_general.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("buildings/", include("mia_buildings.urls")),
    path("people/", include("mia_people.urls")),
    path("facts/", include("mia_facts.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns


admin.site.site_header = "MIA Admin"
admin.site.site_title = "MIA Admin"
admin.site.index_title = "Welcome to MIA Administration"

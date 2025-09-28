from django.contrib.admin.apps import AdminConfig


class MiaAdminConfig(AdminConfig):
    default_site = "modernism.admin.MiaAdminSite"

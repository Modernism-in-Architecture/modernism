from django import template
from home.models import GeneralPage
from wagtail.core.models import Page, Site

register = template.Library()


def is_active(page, current_page):
    return current_page.url_path.startswith(page.url_path) if current_page else False


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


@register.inclusion_tag("tags/main_menu.html", takes_context=True)
def main_menu(context, parent, calling_page=None):
    menuitems = Page.objects.not_type(GeneralPage).live().in_menu()

    for menuitem in menuitems:
        menuitem.is_parent = has_menu_children(menuitem)

        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )

    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        "request": context["request"],
    }


@register.inclusion_tag("tags/second_menu.html", takes_context=True)
def second_menu(context, parent, calling_page=None):
    menuitems = GeneralPage.objects.live().in_menu()

    for menuitem in menuitems:
        menuitem.is_parent = has_menu_children(menuitem)

        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )

    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        "request": context["request"],
    }


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def has_children(page):
    return page.get_children().live().exists()


@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }

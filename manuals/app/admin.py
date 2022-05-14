from app.internal.admin.admin_user import AdminUserAdmin
from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter

from .models import PageElement, PageTreeNode

admin.site.site_title = "Manuals"
admin.site.site_header = "Manuals"


@admin.register(PageElement)
class PageElementAdmin(admin.ModelAdmin):
    list_filter = [("type", AllValuesFieldListFilter)]


@admin.register(PageTreeNode)
class PageTreeNodeAdmin(admin.ModelAdmin):
    pass

from app.internal.infrastructure.db_fill.contents import INFRASTRUCTURE_PAGES, SECTIONS
from django.http import HttpResponseNotFound, JsonResponse
from django.views import View
from app.internal.infrastructure.db_fill.contents import ROOT_PAGE_ID

from app.internal.infrastructure.serialization.page_tree import tree_json

ALL_OPTIONS = SECTIONS.copy()
ALL_OPTIONS.extend(INFRASTRUCTURE_PAGES)


class optionsView(View):
    def get(self, request):
        return JsonResponse({"options": ALL_OPTIONS})


class TreeView(View):
    def get(self, request):
        tree = tree_json(ROOT_PAGE_ID)
        if not tree:
            return HttpResponseNotFound()
        return JsonResponse(tree)

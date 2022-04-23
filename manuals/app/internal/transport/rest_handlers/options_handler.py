from app.internal.infrastructure.db_check.contents import INFRASTRUCTURE_PAGES, SECTIONS
from django.http import JsonResponse
from django.views import View

ALL_OPTIONS = SECTIONS.copy()
ALL_OPTIONS.extend(INFRASTRUCTURE_PAGES)


class optionsView(View):
    def get(self, request):
        return JsonResponse({"options": ALL_OPTIONS})

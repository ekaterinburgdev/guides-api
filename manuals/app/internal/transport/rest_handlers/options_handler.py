from app.internal.infrastructure.db_check.contents import SAMPLE_PAGE, SECTIONS
from django.http import JsonResponse
from django.views import View


class optionsView(View):
    def get(self, request):
        options = {"sample_page": SAMPLE_PAGE, "sections": SECTIONS}
        return JsonResponse(options)

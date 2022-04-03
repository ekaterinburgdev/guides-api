from django.http import Http404, JsonResponse
from django.views import View
from app.models import PageElement
from app.internal.infrastructure.serialization.section_serialization import serialize_page_element


class contentView(View):
    def get(self, request):

        id = "4abb0781ddb941d1b45f9bb16483ef1b"

        pageElement = PageElement.objects.filter(id=id)
        if len(pageElement) > 0:
            pageElement = pageElement.first()
            result_content = serialize_page_element(pageElement)
            return JsonResponse({ "content" : result_content })
        else:
            return Http404()
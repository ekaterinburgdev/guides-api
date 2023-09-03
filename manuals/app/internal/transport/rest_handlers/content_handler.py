from app.internal.infrastructure.serialization.default_page_JSON_serialization import serialize_page_element_by_id
from app.internal.infrastructure.serialization.page_content import get_node_by_url
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views import View


class ContentView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = serialize_page_element_by_id(id)
            if page_content:
                return JsonResponse(page_content)
            else:
                return Http404()
        else:
            return HttpResponseBadRequest("Specify page id at query params")


class UrlContentView(View):
    def get(self, request, suburl):
        node = get_node_by_url(suburl)
        if not node:
            return HttpResponseBadRequest("No such url")
        page_content = serialize_page_element_by_id(node.id)
        if page_content:
            page_content["node_properties"] = node.properties
            return JsonResponse(page_content)
        else:
            return Http404()

from app.internal.infrastructure.serialization.default_page_JSON_serialization import serialize_page_element
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views import View


class contentView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = serialize_page_element(id)
            if page_content:
                return JsonResponse({id: page_content})
            else:
                return Http404()
        else:
            return HttpResponseBadRequest("Specify page id at query params")

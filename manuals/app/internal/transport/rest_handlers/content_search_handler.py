from django.http import HttpResponseBadRequest, HttpRequest, JsonResponse
from django.views import View

DEFAULT_SEARCH_LIMIT = 5
DEFAULT_GUIDE_SUGGESTIONS_LIMIT = 5


class ContentView(View):
    def get(self, request: HttpRequest):
        search_limit = self._get_search_limit_query_param(request)
        guide_suggestions_limit = self._get_guide_suggestions_limit_query_param(request)

        patterns = request.GET.getlist("pattern")
        if not patterns:
            return HttpResponseBadRequest("Specify pattern param at query")
        
        pattern = patterns[0]
        return JsonResponse({"data": "NODATA"})
        # page_content = serialize_page_element_by_id(id)
        # if page_content:
        #     return JsonResponse(page_content)
        # else:
        #     return Http404()
        
    def _get_search_limit_query_param(self, request: HttpRequest) -> str:
        search_limits = request.GET.getlist("search_limit")
        if search_limits:
            return search_limits[0]
        return DEFAULT_SEARCH_LIMIT

    def _get_guide_suggestions_limit_query_param(self, request: HttpRequest) -> str:
        guide_suggestions_limits = request.GET.getlist("guide_suggestions_limit")
        if guide_suggestions_limits:
            return guide_suggestions_limits[0]
        return DEFAULT_GUIDE_SUGGESTIONS_LIMIT
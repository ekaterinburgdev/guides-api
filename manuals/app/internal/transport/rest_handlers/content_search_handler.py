import re
from typing import Dict, List
from django.http import HttpResponseBadRequest, HttpRequest, JsonResponse
from django.views import View

from app.models import PrerenderedPageElement, PageTreeNode

DEFAULT_SEARCH_LIMIT = 5
DEFAULT_GUIDE_SUGGESTIONS_LIMIT = 5
PUNCTS = ",.()[\\]{{}}\"'`<>"


class ContentSearchView(View):
    def get(self, request: HttpRequest):
        search_limit = self._get_search_limit_query_param(request)
        guide_suggestions_limit = self._get_guide_suggestions_limit_query_param(request)

        patterns = request.GET.getlist("pattern")
        if not patterns:
            return HttpResponseBadRequest("Specify pattern param at query")
        
        pattern = patterns[0]
        return JsonResponse(search_pattern(pattern, search_limit, guide_suggestions_limit))
        
    def _get_search_limit_query_param(self, request: HttpRequest) -> int:
        search_limits = request.GET.getlist("search_limit")
        if not search_limits or len(search_limits) < 1 or not search_limits[0].isdigit():
            return DEFAULT_SEARCH_LIMIT
        return int(search_limits[0])

    def _get_guide_suggestions_limit_query_param(self, request: HttpRequest) -> int:
        guide_suggestions_limits = request.GET.getlist("guide_suggestions_limit")
        if not guide_suggestions_limits or len(guide_suggestions_limits) < 1 or not guide_suggestions_limits[0].isdigit():
            return DEFAULT_GUIDE_SUGGESTIONS_LIMIT
        return int(guide_suggestions_limits[0])
    
def search_pattern(pattern: str, search_limit: int, guide_suggestions_limit: int):
    pattern = pattern.strip()
    search_results: List[PrerenderedPageElement] = list(PrerenderedPageElement.objects.filter(text_content__search=pattern))
    all_matches: Dict[str, list] = {}
    for result in search_results:
        guide_id = result.guide_id
        current_guide_matches = all_matches.get(guide_id)
        if current_guide_matches and len(current_guide_matches) >= guide_suggestions_limit:
            continue
        if not current_guide_matches:
            all_matches[guide_id] = []
        matches: List[str] = re.findall(f"((?:[^\\s{PUNCTS}]+[\\s{PUNCTS}]+){{0,5}}[^\\s{PUNCTS}]*{pattern}[^\\s{PUNCTS}]*(?:[\\s{PUNCTS}]+[^\\s{PUNCTS}]*){{0,5}})", result.text_content, re.DOTALL | re.IGNORECASE)
        section_name = result.section_name
        url = result.url
        suggestions = []
        for match in matches[:search_limit]:
            neighbours = re.search(f"(.*){pattern}(.*)", match, re.DOTALL | re.IGNORECASE)
            if neighbours:
                neighbours = neighbours.groups()
            else:
                neighbours = []
            left = ""
            if len(neighbours) > 0:
                left = neighbours[0]
            right = ""
            if len(neighbours) > 1:
                right = neighbours[1]
            link = f"{url}#:~:text={match}"
            if len(suggestions) >= guide_suggestions_limit:
                break
            section_suggestion = {
                "text": {
                    "left": left,
                    "target": pattern,
                    "right": right
                },
                "link": link
            }
            suggestions.append(section_suggestion)
        if len(suggestions) == 0 and len(all_matches[guide_id]) == 0:
            all_matches.pop(guide_id, None)
            continue
        section_suggestion = {
            "sectionName": section_name,
            "suggestions": suggestions
        }
        all_matches[guide_id].append(section_suggestion)
    
    guide_suggestions = []
    for id in all_matches.keys():
        node = PageTreeNode.objects.filter(id=id).first()
        properties = None
        if node:
            properties = node.properties
        guide_suggestion = {
            "properties": properties,
            "sectionSuggestions": all_matches[id]
        }
        guide_suggestions.append(guide_suggestion)
    search_result = {
        "guideSuggestions": guide_suggestions
    }
    return search_result

from app.internal.infrastructure.notion_client import notion_client
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View


class retrieveView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = notion_client.blocks.retrieve(id)
            return JsonResponse(page_content)
        else:
            return HttpResponseBadRequest("Specify page id at query params")


class childrenView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = notion_client.blocks.children.list(id)
            return JsonResponse(page_content)
        else:
            return HttpResponseBadRequest("Specify page id at query params")

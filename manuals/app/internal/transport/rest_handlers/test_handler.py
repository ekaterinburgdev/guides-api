import json

from app.internal.infrastructure.notion_client import NotionClient
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

notion_client = NotionClient().notion_client


class RetrieveView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = notion_client.blocks.retrieve(id)
            return HttpResponse(json.dumps(page_content, indent=4, ensure_ascii=False), content_type="application/json")
        else:
            return HttpResponseBadRequest("Specify page id at query params")


class ChildrenView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = notion_client.blocks.children.list(id)
            return HttpResponse(json.dumps(page_content, indent=4, ensure_ascii=False), content_type="application/json")
        else:
            return HttpResponseBadRequest("Specify page id at query params")


class DbRetrieveView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            page_content = notion_client.databases.retrieve(id)
            return HttpResponse(json.dumps(page_content, indent=4, ensure_ascii=False), content_type="application/json")
        else:
            return HttpResponseBadRequest("Specify page id at query params")


class DbChildrenView(View):
    def get(self, request):
        if request.GET.getlist("id"):
            id = request.GET.getlist("id")[0]
            database_elements = notion_client.databases.query(id)
            return HttpResponse(
                json.dumps(database_elements, indent=4, ensure_ascii=False), content_type="application/json"
            )
        else:
            return HttpResponseBadRequest("Specify page id at query params")

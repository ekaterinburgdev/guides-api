from app.internal.transport.rest_handlers import content_handler, options_handler, test_handler, content_search_handler
from django.urls import path

urlpatterns = [
    path("content", content_handler.ContentView.as_view()),
    path("content/search", content_search_handler.ContentSearchView.as_view()),
    path("content/<path:suburl>", content_handler.UrlContentView.as_view()),
    path("options", options_handler.optionsView.as_view()),
    path("test/retrieve", test_handler.RetrieveView.as_view()),
    path("test/children", test_handler.ChildrenView.as_view()),
    path("test/dbretrieve", test_handler.DbRetrieveView.as_view()),
    path("test/dbchildren", test_handler.DbChildrenView.as_view()),
    path("tree", options_handler.TreeView.as_view()),
    path("test/tree", test_handler.ReadableTreeView.as_view()),
]

from app.internal.transport.rest_handlers import content_handler, options_handler, test_handler
from django.urls import path

urlpatterns = [
    path("content", content_handler.contentView.as_view()),
    path("options", options_handler.optionsView.as_view()),
    path("test/retrieve", test_handler.retrieveView.as_view()),
    path("test/children", test_handler.childrenView.as_view()),
]

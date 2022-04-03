from django.urls import path

from app.internal.transport.rest_handlers import content_handler

urlpatterns = [path("content", content_handler.contentView.as_view())]

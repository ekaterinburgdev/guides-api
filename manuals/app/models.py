from app.internal.models.admin_user import AdminUser
from django.db import models


class PageElement(models.Model):
    id = models.TextField(primary_key=True)
    content = models.JSONField()
    children = models.JSONField()
    type = models.CharField(max_length=30)
    last_edited = models.CharField(max_length=30)

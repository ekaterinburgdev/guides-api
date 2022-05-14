from app.internal.models.admin_user import AdminUser
from django.db import models

# class PageElement(models.Model):
#     id = models.TextField(primary_key=True)
#     content = models.JSONField()
#     children = models.ManyToManyField("PageElement", symmetrical=False)
#     type = models.CharField(max_length=30)
#     last_edited = models.DateTimeField(blank=False)


class PageElement(models.Model):
    id = models.TextField(primary_key=True)
    content = models.JSONField()
    children = models.ManyToManyField("PageElement", symmetrical=False)
    type = models.CharField(max_length=30)
    last_edited = models.DateTimeField(blank=False)


class PageTreeNode(models.Model):
    id = models.TextField(primary_key=True)
    properties = models.JSONField()
    child_page = models.ForeignKey(PageElement, null=True, default=None, on_delete=models.CASCADE)
    child_nodes = models.ManyToManyField("PageTreeNode", symmetrical=False)
    last_edited = models.DateTimeField(blank=False)
    url = models.CharField(max_length=30, null=True, default=None, blank=False, db_index=True)

from app.internal.models.admin_user import AdminUser
from django.db import models


class PageElement(models.Model):
    id = models.TextField(primary_key=True)
    content = models.JSONField()
    children = models.ManyToManyField("PageElement", symmetrical=False)
    type = models.CharField(max_length=70)
    last_edited = models.DateTimeField(blank=False)
    order = models.IntegerField(db_index=True, default=0)


class PageTreeNode(models.Model):
    id = models.TextField(primary_key=True)
    properties = models.JSONField()
    child_page = models.ForeignKey(PageElement, null=True, default=None, on_delete=models.CASCADE)
    child_nodes = models.ManyToManyField("PageTreeNode", symmetrical=False)
    last_edited = models.DateTimeField(blank=False)
    url = models.CharField(max_length=70, null=True, default=None, blank=False, db_index=True)
    show = models.BooleanField(default=True)


class PrerenderedPageElement(models.Model):
    id = models.TextField(primary_key=True)
    guide_id = models.TextField(default="")
    content = models.JSONField()
    nodes_trace = models.JSONField(default=dict)
    section_name = models.TextField(default="")
    text_content = models.TextField(default="")
    url = models.CharField(max_length=70, null=True, default="", blank=False, db_index=True)

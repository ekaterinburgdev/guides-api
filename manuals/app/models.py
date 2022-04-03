from django.db import models

from app.internal.models.admin_user import AdminUser


class PageElement(models.Model):

    class ElementType(models.TextChoices):
        COLUMN_LIST = "ColumnList"
        COLUMN = "Column"
        IMAGE = "Image"
        PARAGRAPH = "Paragraph"
        NONE = "NONE"

    id = models.TextField(primary_key=True)
    content = models.JSONField()
    type = models.CharField(max_length=17, choices=ElementType.choices, default=ElementType.NONE)
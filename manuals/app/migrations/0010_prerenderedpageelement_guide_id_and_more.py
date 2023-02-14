# Generated by Django 4.1 on 2023-01-08 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_prerenderedpageelement_text_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="prerenderedpageelement",
            name="guide_id",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="prerenderedpageelement",
            name="url",
            field=models.CharField(db_index=True, default="", max_length=70, null=True),
        ),
    ]
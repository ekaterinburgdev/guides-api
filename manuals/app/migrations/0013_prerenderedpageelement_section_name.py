# Generated by Django 4.1 on 2023-01-08 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_alter_prerenderedpageelement_nodes_trace"),
    ]

    operations = [
        migrations.AddField(
            model_name="prerenderedpageelement",
            name="section_name",
            field=models.TextField(default=""),
        ),
    ]

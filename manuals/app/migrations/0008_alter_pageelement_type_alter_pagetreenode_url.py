# Generated by Django 4.1 on 2022-12-04 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_prerenderedpageelement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pageelement",
            name="type",
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name="pagetreenode",
            name="url",
            field=models.CharField(db_index=True, default=None, max_length=70, null=True),
        ),
    ]

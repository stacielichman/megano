# Generated by Django 5.0.3 on 2024-05-05 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_sitesettings_is_boolean_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitesettings",
            options={
                "verbose_name": "site setting",
                "verbose_name_plural": "SiteSettings",
            },
        ),
    ]

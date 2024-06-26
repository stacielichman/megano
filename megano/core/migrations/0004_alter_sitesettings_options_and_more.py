# Generated by Django 5.0.3 on 2024-05-12 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_sitesettings_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitesettings",
            options={
                "verbose_name": "настройку сайта",
                "verbose_name_plural": "Настройки сайта",
            },
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="cache_time",
            field=models.IntegerField(default=5, verbose_name="время кеширования"),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="name",
            field=models.CharField(max_length=100, unique=True, verbose_name="имя"),
        ),
    ]

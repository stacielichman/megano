# Generated by Django 5.0.3 on 2024-04-28 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0023_alter_product_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="details",
            field=models.JSONField(
                blank=True, default=dict, verbose_name="Характеристики"
            ),
        ),
    ]

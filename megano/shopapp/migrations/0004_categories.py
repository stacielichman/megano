# Generated by Django 5.0.3 on 2024-03-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shopapp", "0003_alter_seller_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
    ]

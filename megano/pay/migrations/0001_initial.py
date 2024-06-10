# Generated by Django 5.0.3 on 2024-04-03 08:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shopapp", "0013_merge_20240331_1442"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("city", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                (
                    "payment",
                    models.CharField(
                        choices=[("cash", "Cash"), ("credit_card", "Credit Card")],
                        default="cash",
                        max_length=100,
                    ),
                ),
                ("payment_status", models.CharField(max_length=100)),
                (
                    "delivery",
                    models.CharField(
                        choices=[("pickup", "Pickup"), ("courier", "Courier")],
                        default="pickup",
                        max_length=100,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("comment", models.CharField(max_length=200)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("price", models.FloatField()),
                ("old_price", models.FloatField()),
                ("count", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="pay.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="shopapp.productseller",
                    ),
                ),
            ],
        ),
    ]
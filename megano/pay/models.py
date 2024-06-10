from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from shopapp.models import ProductSeller


class PaymentChoices(models.TextChoices):
    CASH = ("cash", _("Cash"))
    CREDIT_CARD = ("credit_card", _("Credit card"))


class DeliveryChoices(models.TextChoices):
    PICKUP = ("pickup", _("Pickup"))
    COURIER = ("courier", _("Courier"))


class PaymentStatus(models.TextChoices):
    PAID = ("paid", _("Paid"))
    CANCELLED = ("cancelled", _("Cancelled"))


class Order(models.Model):
    class Meta:
        get_latest_by = "created_at"
        verbose_name = _("заказ")
        verbose_name_plural = _("Заказы")

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("пользователь"),
    )
    city = models.CharField(max_length=100, verbose_name=_("город"))
    address = models.CharField(max_length=100, verbose_name=_("адрес"))
    payment_type = models.CharField(
        choices=PaymentChoices.choices,
        default=PaymentChoices.CASH,
        max_length=100,
        verbose_name=_("оплата"),
    )
    payment_status = models.CharField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.CANCELLED,
        max_length=100,
        verbose_name=_("статус оплаты"),
    )
    delivery = models.CharField(
        choices=DeliveryChoices.choices,
        default=DeliveryChoices.PICKUP,
        max_length=100,
        verbose_name=_("доставка"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("создан"))
    comment = models.CharField(max_length=200, verbose_name=_("комментарий"))
    reference_num = models.CharField(max_length=100, verbose_name=_("номер заказа"))


class OrderItem(models.Model):
    class Meta:
        verbose_name = _("заказ-товар")
        verbose_name_plural = _("Заказы-товары")

    order = models.ForeignKey(
        Order,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name=_("заказ"),
    )
    price = models.FloatField(verbose_name=_("цена"))
    old_price = models.FloatField(verbose_name=_("старая цена"))
    count = models.IntegerField(verbose_name=_("количество"))
    product = models.ForeignKey(
        ProductSeller,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("продукт"),
    )


class Transaction(models.Model):
    class Meta:
        verbose_name = _("транзакцию")
        verbose_name_plural = _("Транзакции")

    uuid = models.CharField(max_length=100, verbose_name=_("uuid"))
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("сумма")
    )
    payment_status = models.CharField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.CANCELLED,
        max_length=100,
        verbose_name=_("статус оплаты"),
    )
    order = models.ForeignKey(
        Order,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="transaction",
        verbose_name=_("заказ"),
    )
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.PROTECT,
        related_name="transaction",
        verbose_name=_("пользователь"),
    )

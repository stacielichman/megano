from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Seller(models.Model):
    class Meta:
        verbose_name = _("продавца")
        verbose_name_plural = _("Продавцы")

    name = models.CharField(max_length=255, verbose_name=_("имя"))
    description = models.CharField(max_length=255, verbose_name=_("описание"))
    image = models.ImageField(
        upload_to="seller_image_directory_path",
        blank=True,
        null=True,
        verbose_name=_("картинка"),
    )
    phone = models.IntegerField(verbose_name=_("номер телефона"))
    address = models.CharField(max_length=255, verbose_name=_("адрес"))
    email = models.EmailField(verbose_name=_("email"))

    def __str__(self):
        return self.name


def seller_image_directory_path(instance: "Seller", filename: str) -> str:
    return "sellers/seller_{pk}/image/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Categories(models.Model):
    class Meta:
        verbose_name = _("категорию")
        verbose_name_plural = _("Категории")

    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("имя"))
    archived = models.BooleanField(default=False, verbose_name=_("архивирован"))
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/images/{filename}".format(
        filename=filename,
    )


class ProductImage(models.Model):
    """
    Модель ProductImage представляет изображение продукта.
    """

    class Meta:
        verbose_name = _("продукт-картинку")
        verbose_name_plural = _("Продукты-картинки")

    image = models.ImageField(
        upload_to=product_images_directory_path, verbose_name=_("картинка")
    )
    is_preview = models.BooleanField(default=False, verbose_name=_("предпросмотр"))


class Product(models.Model):
    """
    Модель Product представляет товар,
    который можно продавать в интернет-магазине.
    """

    class Meta:
        verbose_name = _("продукт")
        verbose_name_plural = _("Продукты")

    name = models.CharField(max_length=100, db_index=True, verbose_name=_("имя"))
    description = models.TextField(null=False, blank=True, verbose_name=_("описание"))
    archived = models.BooleanField(default=False, verbose_name=_("архивирован"))
    preview = models.ForeignKey(
        ProductImage, on_delete=models.CASCADE, verbose_name=_("предпросмотр")
    )
    images = models.ManyToManyField(
        ProductImage, blank=True, related_name="products", verbose_name=_("картинки")
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
        related_name="product_category",
        verbose_name=_("категория"),
    )
    details = models.JSONField(blank=True, verbose_name=_("детали"), default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


class ProductSeller(models.Model):
    """
    Модель ProductSeller представляет продукт с его ценой от продавца
    """

    class Meta:
        verbose_name = _("продукт-продавца")
        verbose_name_plural = _("Продукты-продавцы")

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="product_sellers",
        verbose_name=_("продукт"),
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.PROTECT, verbose_name=_("продавец")
    )
    price = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, verbose_name=_("цена")
    )
    quantity = models.SmallIntegerField(default=0, verbose_name=_("количество"))
    sale = models.IntegerField(blank=True, default=0, verbose_name=_("скидка"))

    def get_sale(self):
        """Функция рассчитывает стоимость со скидкой"""
        price = int(self.price * (100 - self.sale) / 100)
        return price


class ViewHistory(models.Model):
    """
    Модель ViewHistory представляет историю просмотренных продуктов
    """

    class Meta:
        verbose_name = _("просмотр истории")
        verbose_name_plural = _("Просмотр историй")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="view_history",
        verbose_name=_("пользователь"),
    )
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("дата создания")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="view_historys",
        verbose_name=_("дата создания"),
    )


def discount_img_directory_path(instance: "Discount", filename: str) -> str:
    return "discounts/discount_{pk}/image/{filename}".format(
        pk=instance.pk, filename=filename
    )


class DiscountTypeChoices(models.TextChoices):
    PERCENT = ("%", "%")
    RUBLES = ("RUB", _("RUB"))


class Discount(models.Model):
    """
    Модель ViewHistory представляет скидку на продукт
    """

    class Meta:
        verbose_name = _("скидку")
        verbose_name_plural = _("Скидки")

    name = models.CharField(max_length=255, verbose_name=_("имя"))
    description = models.TextField(null=False, blank=True, verbose_name=_("описание"))
    products = models.ManyToManyField(Product, verbose_name=_("продукты"))
    date_start = models.DateTimeField(auto_now_add=True, verbose_name=_("дата начала"))
    date_end = models.DateTimeField(verbose_name=_("дата конца"))
    promocode = models.CharField(max_length=255, verbose_name=_("промокод"))
    is_group = models.BooleanField(default=False, verbose_name=_("группа"))
    is_active = models.BooleanField(default=False, verbose_name=_("активная"))
    value = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, verbose_name=_("значение")
    )
    type = models.CharField(
        choices=DiscountTypeChoices.choices,
        default=DiscountTypeChoices.PERCENT,
        max_length=100,
        verbose_name=_("тип"),
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=discount_img_directory_path,
        verbose_name=_("картинка"),
    )

    def __str__(self) -> str:
        return f"Discount(pk={self.pk}, name={self.name!r})"


class Review(models.Model):
    """Модель Review представляет отзывы на продукт"""

    class Meta:
        verbose_name = _("отзыв")
        verbose_name_plural = _("Отзывы")

    author = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, verbose_name=_("автор")
    )
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.PROTECT,
        related_name="reviews_product",
        verbose_name=_("продукт"),
    )
    content = models.TextField(null=False, blank=True, verbose_name=_("содержание"))
    created_reviews = models.DateTimeField(
        auto_now_add=True, verbose_name=_("созданные отзывы")
    )


def avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "users/user_{pk}/avatar/{filename}".format(pk=instance.pk, filename=filename)


class Profile(models.Model):
    """
    Модель Profile представляет профиль пользователя
    """

    default_phone_validator = RegexValidator(
        r"\+(\d){1,3} \((\d){2,3}\) (\d{3}) (\d{2}) (\d){2}$",
        message=_("Введите правильный номер. Пример: +7 (999) 999 99 99"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("пользователь")
    )
    avatar = models.ImageField(
        null=True, blank=True, upload_to=avatar_directory_path, verbose_name=_("аватар")
    )
    default_phone_validator = RegexValidator(
        r"\+(\d){1,3} \((\d){2,3}\) (\d{3}) (\d{2}) (\d){2}$",
        message=_("Введите правильный номер. Пример: +7 (999) 999 99 99"),
    )
    phone = models.CharField(
        validators=[default_phone_validator], max_length=60, null=True, blank=True
    )
    middle_name = models.CharField(
        max_length=255, verbose_name=_("отчество"), null=True
    )
    seller = models.ForeignKey(
        Seller,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("продавец"),
    )

    class Meta:
        verbose_name = _("профиль")
        verbose_name_plural = _("Профили")


def banner_image_directory_path(instance: "Banner", filename: str) -> str:
    return "banners/banner_{pk}/{filename}".format(pk=instance.pk, filename=filename)


class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image = models.ImageField(
        null=True, blank=True, upload_to=banner_image_directory_path
    )
    is_active = models.BooleanField(default=False)
    is_big = models.BooleanField(default=False)

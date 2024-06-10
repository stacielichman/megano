from decimal import Decimal

from django.conf import settings

from shopapp.models import ProductSeller


class Cart(object):
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_seller, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_seller_id = str(product_seller.id)
        if product_seller_id not in self.cart:
            self.cart[product_seller_id] = {
                "quantity": 0,
                "price": str(product_seller.price),
                "old_price": str(product_seller.price),
            }
        if update_quantity:
            self.cart[product_seller_id]["quantity"] = quantity
        else:
            self.cart[product_seller_id]["quantity"] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product_seller):
        """
        Удаление товара из корзины.
        """
        product_seller = str(product_seller.id)
        if product_seller in self.cart:
            del self.cart[product_seller]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_seller_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        product_sellers = ProductSeller.objects.filter(id__in=product_seller_ids)
        for product_seller in product_sellers:
            self.cart[str(product_seller.id)]["product_seller"] = product_seller

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["old_price"] = Decimal(item["old_price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

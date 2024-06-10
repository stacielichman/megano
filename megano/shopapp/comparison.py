from decimal import Decimal

from django.conf import settings

from .models import Product, ProductImage, ProductSeller


class Comparison(object):
    def __init__(self, request):
        """
        Инициализируем сравнение
        """
        self.session = request.session
        compare = self.session.get(settings.COMPARISON_SESSION_ID)
        if not compare:
            # save an empty compare in the session
            compare = self.session[settings.COMPARISON_SESSION_ID] = {}
        self.compare = compare

    def add(self, product_seller):
        """
        Добавить продукт в список для сравнения.
        """

        product = product_seller.product
        product_id = str(product.id)
        try:
            img = self.get_more_about_product(product.id)
        except:
            img = None
        if product_id not in self.compare:
            self.compare[product_id] = {
                "id": product.id,
                "name": product.name,
                "details": product.details,
                "price": float(product_seller.price),
                "img": img,
            }
        self.save()

    def save(self):
        # Обновление сессии compare
        self.session[settings.COMPARISON_SESSION_ID] = self.compare
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product_seller):
        """
        Удаление товара из сравнения.
        """
        product_id = str(product_seller.product.id)
        if product_id in self.compare:
            del self.compare[product_id]
            self.save()

    def get_more_about_product(self, product_id):
        """
        Получить путь к img и другую информацию о продукте
        """
        img = ProductImage.objects.filter(product_id=product_id).select_related(
            "product_images"
        )
        return img

    @staticmethod
    def get_similar(products: tuple) -> dict:
        similar = {str(product.get("id")): [] for product in products}
        for index_check in range(len(products) - 1):
            check_details = products[index_check].get("details")
            for curr_i in range(index_check + 1, len(products)):
                curr_details = products[curr_i].get("details")
                for detail, value in curr_details.items():
                    if detail in check_details.keys():
                        if curr_details.get(detail) == check_details.get(detail):
                            similar[str(products[index_check].get("id"))].append(detail)
                            similar[str(products[curr_i].get("id"))].append(detail)
        return similar

    def __iter__(self):
        """
        Перебор элементов в сравнении и получение продуктов из базы данных.
        """
        product_ids = self.compare.keys()
        # получение объектов product и добавление их в сравнение
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.compare[str(product.id)]["img"] = product.preview.image.url
        for item in self.compare.values():
            yield item

    def __len__(self):
        """
        Подсчет всех элементов в сравнении.
        """
        return len(self.compare)

    def clear(self):
        # удаление сравнения из сессии
        del self.session[settings.COMPARISON_SESSION_ID]
        self.session.modified = True

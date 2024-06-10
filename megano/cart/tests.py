from django.test import TestCase
from django.urls import reverse


class CartAddTestCase(TestCase):
    def test_cart_add(self):
        responce = self.client.get(reverse("cart:cart_add"))
        self.assertEqual(responce.status_code, 200)


class AddInsideCartTestCase(TestCase):
    def test_add_inside_cart(self):
        responce = self.client.get(reverse("cart:add_inside_cart"))
        self.assertEqual(responce.status_code, 200)


class RemoveInsideCartTestCase(TestCase):
    def test_remove_inside_cart(self):
        responce = self.client.get(reverse("cart:remove_inside_cart"))
        self.assertEqual(responce.status_code, 200)


class CartDetailTestCase(TestCase):
    def test_cart_detail(self):
        responce = self.client.get(reverse("cart:cart_detail"))
        self.assertEqual(responce.status_code, 200)

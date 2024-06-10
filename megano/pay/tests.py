from django.test import TestCase
from django.urls import reverse


class OrderStep1TestCase(TestCase):
    def test_order_step_1(self):
        responce = self.client.get(reverse("pay:step_1"))
        self.assertEqual(responce.status_code, 200)


class OrderStep2TestCase(TestCase):
    def test_order_step_2(self):
        responce = self.client.get(reverse("pay:step_2"))
        self.assertEqual(responce.status_code, 200)


class OrderStep3TestCase(TestCase):
    def test_order_step_3(self):
        responce = self.client.get(reverse("pay:step_3"))
        self.assertEqual(responce.status_code, 200)


class OrderStep4TestCase(TestCase):
    def test_order_step_4(self):
        responce = self.client.get(reverse("pay:step_4"))
        self.assertEqual(responce.status_code, 200)


class PaymentCardTestCase(TestCase):
    def test_product_card(self):
        responce = self.client.get(reverse("pay:payment"))
        self.assertEqual(responce.status_code, 200)


class PaymentInvoiceTestCase(TestCase):
    def test_payment_invoice(self):
        responce = self.client.get(reverse("pay:paymentsomeone"))
        self.assertEqual(responce.status_code, 200)


class ProofPaymentTestCase(TestCase):
    def test_proof_payment(self):
        responce = self.client.get(reverse("pay:progressPayment"))
        self.assertEqual(responce.status_code, 200)

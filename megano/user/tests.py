from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class LoginTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            username="username_test",
            password="password",
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_login(self):
        responce = self.client.get(reverse("auth:login"))
        self.assertEqual(responce.status_code, 200)


class RegisterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_register = User.objects.create(
            username="username_test",
            password="password",
        )

    @classmethod
    def tearDownClass(cls):
        cls.user_register.delete()

    def test_register(self):
        responce = self.client.get(reverse("auth:register"))
        self.assertEqual(responce.status_code, 200)


class LogoutTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_logout = User.objects.create(
            username="username_test",
            password="password",
        )

    @classmethod
    def tearDownClass(cls):
        cls.user_logout.delete()

    def test_register(self):
        responce = self.client.get(reverse("auth:logout"))
        self.assertEqual(responce.status_code, 200)


class ResetPasswordTestCase(TestCase):
    def test_reset_password(self):
        responce = self.client.get(reverse("auth:recovery_password"))
        self.assertEqual(responce.status_code, 200)


class ResetPasswordDoneTestCase(TestCase):
    def test_reset_password_done(self):
        responce = self.client.get(reverse("auth:password_reset_done"))
        self.assertEqual(responce.status_code, 200)


class ResetPasswordConfirmTestCase(TestCase):
    def test_reset_password_confirm(self):
        responce = self.client.get(reverse("auth:password_reset_confirm"))
        self.assertEqual(responce.status_code, 200)


class ResetPasswordCompleteTestCase(TestCase):
    def test_reset_password_complete(self):
        responce = self.client.get(reverse("auth:password_reset_complete"))
        self.assertEqual(responce.status_code, 200)

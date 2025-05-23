from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Pop", email="john@mail.ru", password="123"
        )

    def test_login(self):
        responce = self.client.get("/users/1/update/")
        self.assertEqual(responce.status_code, 302)


class TestRegistration(TestCase):
    def test_registration(self):
        responce = self.client.post(
            reverse("registration"),
            {
                "username": "NewUser",
                "email": "newuser@mail.ru",
                "password1": "123",
                "password2": "123",
            },
        )
        self.assertEqual(responce.status_code, 302)
        self.assertTrue(User.objects.filter(username="NewUser").exists())


class TestUserUpdate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Pop", email="john@mail.ru", password="123"
        )
        self.client.login(username="Pop", password="123")

    def test_update_user(self):
        responce = self.client.post(
            reverse("update_user", args=[self.user.id]),
            {
                "username": "UpdateUser",
                "email": "update@mail.ru",
                "password1": "456",
                "password2": "456",
            },
        )
        self.assertEqual(responce.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "UpdateUser")


class TestUserDelete(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Pop", email="john@mail.ru", password="123"
        )
        self.client.login(username="Pop", password="123")

    def test_delete_user(self):
        responce = self.client.post(reverse("delete_user", args=[self.user.id]))
        self.assertEqual(responce.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

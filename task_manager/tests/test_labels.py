from django.test import TestCase
from task_manager.labels.models import Label
from django.urls import reverse


class TestsLables(TestCase):
    def setUp(self):
        self.label = Label.objects.create(
            name="Test Lable", description="Test Description"
        )

    def test_create_label(self):
        responce = self.client.post(
            reverse("create_label"),
            {
                "name": "New Label",
                "description": "New Description",
            },
        )
        self.assertEqual(responce.status_code, 302)
        self.assertTrue(Label.objects.filter(name="New Label").exists())

    def test_update_label(self):
        responce = self.client.post(
            reverse("update_label", args=[self.label.pk]),
            {
                "name": "Update Label",
                "description": "Update Description",
            },
        )
        self.assertEqual(responce.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Update Label")

    def test_delete_label(self):
        responce = self.client.post(reverse("delete_label", args=[self.label.pk]))
        self.assertEqual(responce.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

from django.test import TestCase
from statuses.models import Status
from django.contrib.auth.models import User
from django.urls import reverse

class TestsStatuses(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Mno1b')

    def test_create_status(self):
        response = self.client.post(reverse('create_status'), {
            'name': 'Mroh2d',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Mroh2d').exists())

    def test_update_status(self):
        response = self.client.post(reverse('update_status', args=[self.status.pk]), {
            'name': 'ghytr3',
        })
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'ghytr3')

    def test_delete_status(self):
        response = self.client.post(reverse('delete_status', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
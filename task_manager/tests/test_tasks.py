from django.test import TestCase
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from django.urls import reverse


class TestTask(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.status = Status.objects.create(name="In Progress")
        self.label = Label.objects.create(name="Important")
        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test Task",
            status=self.status,
            author=self.user,
            assignee=self.user,
        )
        self.task.labels.add(self.label)

    def test_create_task(self):
        response = self.client.post(
            reverse("create_task"),
            {
                "name": "New Task",
                "description": "This is a description",
                "status": self.status.pk,
                "assignee": self.user.pk,
                "labels": [self.label.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_update_task(self):
        response = self.client.post(
            reverse("update_task", args=[self.task.pk]),
            {
                "name": "Update Task",
                "description": "This is an update task",
                "status": self.status.pk,
                "assignee": self.user.pk,
                "labels": [self.label.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Update Task")

    def test_delete_task(self):
        response = self.client.post(reverse("delete_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class TaskTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="New")
        self.author = User.objects.create_user(
            username="author", password="password"
        )
        self.executor = User.objects.create_user(
            username="executor", password="password"
        )

    def test_task_creation(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            author=self.author,
            executor=self.executor,
        )
        self.assertEqual(Task.objects.count(), 1)

    def test_no_tasks_after_creation(self):
        self.assertEqual(Task.objects.count(), 0)

    def test_task_creation_after_previous_test(self):
        Task.objects.create(
            name="Another Test Task",
            description="Another Test Description",
            status=self.status,
            author=self.author,
            executor=self.executor,
        )
        self.assertEqual(Task.objects.count(), 1)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.ru",
        )
        self.course = Course.objects.create(
            title="Курс тест", description="Тест", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Урок тест",
            description="Тест",
            link_to_the_video="http://youtube.com/test",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест информации об одном уроке"""

        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("description"), self.lesson.description)
        self.assertEqual(data.get("link_to_the_video"), self.lesson.link_to_the_video)
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("owner"), self.lesson.owner.id)

    def test_lesson_create(self):
        """Тест создания урока"""

        url = reverse("materials:lesson-create")
        data = {
            "title": "Урок тест1",
            "description": "Тест1",
            "link_to_the_video": "http://youtube.com/test",
            "course": 1,
            "owner": 1,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест обновление урока"""

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Урок тест2"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок тест2")

    def test_lesson_delete(self):
        """Тестирование удаления урока"""

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест списка уроков"""

        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 4,
                    "link_to_the_video": "http://youtube.com/test",
                    "title": "Урок тест",
                    "description": "Тест",
                    "preview": None,
                    "course": 3,
                    "owner": 3,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@mail.ru")
        self.course = Course.objects.create(
            title="Курс тест1", description="Тест1", owner=self.user
        )
        # self.subscription = Subscription.objects.create(user=self.user, course=self.course, subscription_flag=True)
        self.client.force_authenticate(user=self.user)

    def test_add_sub(self):
        """Тест добавления подписки"""

        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)

from django.contrib.auth.models import Group
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from lms.models import Lesson, Course, CourseSubscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create(id=1, email='test@test.com', password='123123')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='test_course', description='test_desc')
        self.lesson = Lesson.objects.create(title='test_lesson', description='test_desc',
                                            link='https://youtube.com/',
                                            course=self.course, owner=self.user)

    def test_create_lesson(self):
        data = {'title': 'test', 'description': 'test',
                'course': self.course.id, 'url': 'https://youtube.com/',
                'owner': self.user.id}
        url = reverse('lms:create_lesson')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title=data['title']).exists())

    def test_retrieve_lesson(self):
        url = reverse('lms:view_lesson', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        url = reverse('lms:update_lesson', kwargs={'pk': self.lesson.pk})
        data = {'title': 'Updating_test', 'description': 'Updating_test'}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data['title'])

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse('lms:delete_lesson', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.count(),
            0
        )


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@sky.pro', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )
        self.subscription = CourseSubscription.objects.create(
            owner=self.user,
            course=self.course,
        )

    def test_subscription_create(self):
        course = Course.objects.create(title='Test course 2')
        course.save()

        data = {
            'course': course.id,
            'owner': self.user.id
        }
        response = self.client.post(
            reverse('lms:subs_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            CourseSubscription.objects.count(),
            2
        )

    def test_subscription_list(self):
        response = self.client.get(
            reverse('lms:subs_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': self.subscription.id, 'is_subscribed': False, 'course': self.subscription.course.id,
              'owner': self.subscription.owner.id}]
        )

    def test_subscription_delete(self):
        response = self.client.delete(
            reverse('lms:subs_delete', args=[self.subscription.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            CourseSubscription.objects.count(),
            0
        )

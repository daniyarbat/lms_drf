from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Course, Lesson, CourseSubscription
from lms.paginators import LessonPaginator, CoursePaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from lms.tasks import send_course_update, send_lesson_adding


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course_id = serializer.save(owner=self.request.user).id
        send_course_update.delay(course_id)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]
    pagination_class = LessonPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        course_id = serializer.save(owner=self.request.user).course.id
        lesson_id = serializer.save().id
        send_lesson_adding.delay(lesson_id, course_id)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return CourseSubscription.objects.filter(owner=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

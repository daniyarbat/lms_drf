from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson, CourseSubscription
from lms.paginators import LessonPaginator, CoursePaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer


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


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]
    pagination_class = LessonPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return CourseSubscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

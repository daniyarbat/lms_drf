from django.urls import path
from rest_framework import routers

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, SubscriptionListAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = LmsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='view_lesson'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete_lesson'),

    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subs-list'),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subs-create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subs-delete'),
] + router.urls

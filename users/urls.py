from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views
from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='пользователи')

urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payments'),
] + router.urls

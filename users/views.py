from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.permissions import IsOwner, IsModerator
from lms.services import create_product, create_price
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('payed_lesson', 'payed_course', 'payment_type',)
    ordering_fields = ('date_of_payment', 'amount',)


class PaymentCreateAPIView(APIView):

    def post(self, request, format=None):  # Получаем данные о платеже из запроса

        user = request.user
        amount = request.data.get('amount')
        payment_type = request.data.get('payment_type')

        product_id = create_product("Course Subscription", "Subscription to course")  # Создаем продукт в Stripe
        price_id = create_price(product_id, amount, 'RUB')  # Создаем цену в Stripe

        payment_date = timezone.now()
        payment = Payment.objects.create(user=user, amount=amount, payment_type=payment_type,
                                          product_id=product_id, price_id=price_id, payment_date=payment_date)

        success_url = "http://example.com/success"
        cancel_url = "http://example.com/cancel"
        session_url = payment.create_checkout_session(success_url, cancel_url)  # Создаем сессию для платежа в Stripe

        if session_url:   # Если сессия создана успешно, возвращаем URL для оплаты
            return Response({'session_url': session_url}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create checkout session'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusAPIView(APIView):
    def get(self, request, pk, format=None):

        payment = Payment.objects.get(pk=pk)
        return Response({'status': 'Payment status goes here'}, status=status.HTTP_200_OK)

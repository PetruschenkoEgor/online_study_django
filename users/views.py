from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.permissions import IsOwnerUser
from users.serializers import (PaymentsSerializer, UserInfoSerializer,
                               UserSerializer)


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Переопределяем логику сохранения пользователя"""

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Информация о пользователе"""

    serializer_class = UserInfoSerializer
    queryset = User.objects.all()


class UserListAPIView(ListAPIView):
    """Список пользователей"""

    serializer_class = UserInfoSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Обновление пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwnerUser,)


class UserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = User.objects.all()


class PaymentsCreateAPIView(CreateAPIView):
    """Создание платежа"""

    serializer_class = PaymentsSerializer


class PaymentsRetrieveAPIView(RetrieveAPIView):
    """Информация о платеже"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    """Список платежей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["paid_course__title", "paid_lesson__title"]
    ordering_fields = ["payment_date"]
    filterset_fields = ["payment_method"]

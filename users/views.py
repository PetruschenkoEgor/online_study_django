from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    """Вьюсет для пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


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

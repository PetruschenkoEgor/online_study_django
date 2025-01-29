from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:

        model = User
        fields = "__all__"


class UserInfoSerializer(ModelSerializer):
    """Общая информация о пользователе"""

    class Meta:

        model = User
        fields = ("id", "first_name", "email", "phone", "country", "avatar")


class PaymentsSerializer(ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:

        model = Payments
        fields = "__all__"

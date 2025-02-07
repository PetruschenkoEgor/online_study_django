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
        fields = [
            "id",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "payment_amount",
            "payment_method",
            "session_id",
            "link",
        ]
        read_only_fields = ["id", "payment_date", "session_id", "link"]

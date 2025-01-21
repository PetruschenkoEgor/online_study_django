from rest_framework.serializers import ModelSerializer

from users.models import User, Payments


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:

        model = User
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    """ Сериализатор для платежей """

    class Meta:

        model = Payments
        fields = '__all__'

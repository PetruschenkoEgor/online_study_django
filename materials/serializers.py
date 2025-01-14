from rest_framework.serializers import ModelSerializer

from materials.models import Course


class CourseSerializer(ModelSerializer):
    """ Сериалайзер для модели Курса """

    class Meta:
        model = Course
        fields = '__all__'

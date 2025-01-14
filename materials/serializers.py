from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """ Сериалайзер для модели Курса """

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    """ Сериалайзер для модели Урока """

    class Meta:
        model = Lesson
        fields = '__all__'

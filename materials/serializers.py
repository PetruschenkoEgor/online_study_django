from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Курса"""

    # поле вывода количества уроков
    count_quantity_lessons = SerializerMethodField()

    def get_count_quantity_lessons(self, course):
        """ Количество уроков для определенного курса """

        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Урока"""

    class Meta:
        model = Lesson
        fields = "__all__"

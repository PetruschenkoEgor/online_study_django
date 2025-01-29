from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Урока"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Курса"""

    # поле вывода количества уроков
    count_quantity_lessons = SerializerMethodField()
    # поле вывода информации обо всех уроках
    lessons_info = LessonSerializer(many=True, read_only=True, source="lessons")

    def get_count_quantity_lessons(self, course):
        """Количество уроков для определенного курса"""

        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "count_quantity_lessons",
            "lessons_info",
            "owner",
        ]

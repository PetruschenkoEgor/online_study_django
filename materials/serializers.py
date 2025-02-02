from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_link


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урока"""

    # только http://youtube.com
    link_to_the_video = serializers.CharField(validators=[validate_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курса"""

    # поле вывода количества уроков
    count_quantity_lessons = serializers.SerializerMethodField()
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

from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_link


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урока"""

    # только http://youtube.com
    link_to_the_video = serializers.CharField(validators=[validate_link])

    class Meta:
        model = Lesson
        fields = "__all__"


# class SubscriptionSerializer(serializers.ModelSerializer):
#     """ Сериализатор для модели Подписки """
#
#     sub_user = serializers.SerializerMethodField()
#
#     def get_sub_user(self):
#         """ Подписан пользователь или нет """
#
#         return Subscription.objects.filter(user=self.request.user)
#
#     class Meta:
#         model = Subscription
#         fields = [
#             'user',
#             'sub_user'
#         ]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курса"""

    # поле вывода количества уроков
    count_quantity_lessons = serializers.SerializerMethodField()
    # поле для вывода подписки
    is_sub_user = serializers.SerializerMethodField()
    # поле вывода информации обо всех уроках
    lessons_info = LessonSerializer(many=True, read_only=True, source="lessons")

    def get_count_quantity_lessons(self, course):
        """Количество уроков для определенного курса"""

        return Lesson.objects.filter(course=course).count()

    def get_is_sub_user(self, course):
        """Подписан пользователь или нет"""

        user = self.context["request"].user
        is_sub = Subscription.objects.filter(user=user, course=course).first()
        if is_sub:
            return is_sub.subscription_flag
        return False

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
            "is_sub_user",
        ]

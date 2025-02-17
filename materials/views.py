from __future__ import absolute_import, unicode_literals

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_mail_after_update_course
from users.models import User
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    """Вьюсет для модели Курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Привязка пользователя при создании курса"""

        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Проверка прав доступа"""

        if self.action == "create":
            self.permission_classes = [~IsModer, IsAuthenticated]
        elif self.action == "destroy":
            self.permission_classes = [~IsModer | IsOwner, IsAuthenticated]
        elif self.action in ["retrieve", "list", "update"]:
            self.permission_classes = [IsOwner | IsModer, IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """Если пользователь модератор, возвращаем все курсы, если нет, то только курсы текущего пользователя"""

        if self.request.user.groups.filter(name="moders").exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    @action(detail=True, methods=("patch", "put"))
    def updated(self, request, pk):
        """Если курс обновляется, то пользователю приходит оповещение."""

        # Обновление объекта курса
        response = self.partial_update(request, pk)

        # Получение подписчиков курса
        subscriptions = Subscription.objects.filter(course=pk, subscription_flag=True)
        email_list = [subscription.user.email for subscription in subscriptions]

        # Отправляем уведомление подписчикам об обновлении курса
        send_mail_after_update_course.delay(email_list)
        return response


class LessonCreateAPIView(CreateAPIView):
    """Создание Урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ~IsModer,
    ]

    def perform_create(self, serializer):
        """Привязка пользователя при создании урока"""

        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """Информация об уроке"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

    def get_queryset(self):
        """Если пользователь модератор, возвращаем все уроки, если нет, то только уроки текущего пользователя"""

        if self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Все уроки"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Если пользователь модератор, возвращаем все уроки, если нет, то только уроки текущего пользователя"""

        if self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def get_queryset(self):
        """Если пользователь модератор, возвращаем все уроки, если нет, то только уроки текущего пользователя"""

        if self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer | IsOwner]

    def get_queryset(self):
        """Если пользователь модератор, возвращаем все уроки, если нет, то только уроки текущего пользователя"""

        if self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """Добавление и удаление подписки пользователя на обновления"""

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(Q(user=user) & Q(course=course_item))

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item, subscription_flag=True
            )
            message = "Подписка добавлена"
        return Response({"message": message})

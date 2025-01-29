from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    """Вьюсет для модели Курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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

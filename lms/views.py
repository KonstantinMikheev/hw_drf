from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Course."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        """Возвращает объекты в зависимости от прав доступа."""
        if self.request.user.groups.filter(name="moderators"):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user.pk)

    def get_permissions(self):
        """Возвращает список разрешений, требуемых для пользователей группы moderators."""
        if self.action == "create":
            self.permission_classes = (IsAuthenticated & ~IsModerator,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (
                IsAuthenticated & IsOwner | IsModerator,
            )
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated & IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки владельца к создаваемому объекту."""
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    """Представление для создания новых объектов модели Lesson."""
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModerator,)

    def perform_create(self, serializer):
        """Переопределение метода для автоматической привязки владельца к создаваемому объекту."""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Представление для просмотра объектов модели Lesson."""
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)

    def get_queryset(self):
        """Возвращает объекты в зависимости от прав доступа."""
        if self.request.user.groups.filter(name="moderators"):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user.pk)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра одного объекта модели Lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Представление для изменения объекта модели Lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления объекта модели Lesson."""
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsOwner,)

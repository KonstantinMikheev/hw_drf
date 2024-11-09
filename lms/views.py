from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.tasks import send_email_to_subs_after_updating_course
from users.permissions import IsModerator, IsOwner


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Получение списка доступных курсов"
))
class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Course."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

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

    def perform_update(self, serializer):
        """Переопределение метода для отправки сообщения об обновлении курса"""
        instance = serializer.save()
        send_email_to_subs_after_updating_course.delay(instance.pk)


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
    pagination_class = LessonPaginator

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


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        sub_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if sub_item.exists():
            sub_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
        return Response({"message": message})
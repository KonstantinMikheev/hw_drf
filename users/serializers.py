from rest_framework import serializers

from lms.serializers import LessonSerializer, CourseSerializer
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments_history = PaymentSerializer(many=True, source='payment_set', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city', 'is_active', 'payments_history',)

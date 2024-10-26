from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments_history = PaymentSerializer(
        many=True, source="payment_set", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "email",
            "phone",
            "groups",
            "avatar",
            "city",
            "is_active",
            "is_superuser",
            "is_staff",
            "payments_history",
            "password",
        )

# class UserLimitedSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = (
#             "pk",
#             "first_name",
#             "email",
#             "city",
#             "is_active",
#         )

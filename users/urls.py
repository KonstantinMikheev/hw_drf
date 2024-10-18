from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
                  path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
                  path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-detail'),
              ]
urlpatterns += router.urls

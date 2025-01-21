from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsCreateAPIView, PaymentsRetrieveAPIView, PaymentsListAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),
    path('payments/<int:pk>/', PaymentsRetrieveAPIView.as_view(), name='payment-get'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
]

urlpatterns += router.urls

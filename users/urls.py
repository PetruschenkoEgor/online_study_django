from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentsCreateAPIView, PaymentsListAPIView,
                         PaymentsRetrieveAPIView, UserCreateAPIView,
                         UserDestroyAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "personal_account/<int:pk>/",
        UserRetrieveAPIView.as_view(),
        name="personal_account",
    ),
    path("accounts/", UserListAPIView.as_view(), name="accounts"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="delete"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments-create"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payment-get"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments-list"),
]

from django.urls import path
from .views import (
    UserRegistrationAPIView,
    LoginAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    PasswordChangeAPIView,
    LogoutAPIView,
    UserDeleteAPIView,
)


urlpatterns = [
    # Any user can access.
    path(route="registration/", view=UserRegistrationAPIView.as_view()),
    path(route="login/", view=LoginAPIView.as_view()),
    # Authenticated users only can access.
    path(route="detail/", view=UserDetailAPIView.as_view()),
    path(route="update/", view=UserUpdateAPIView.as_view()),
    path(route="password-change/", view=PasswordChangeAPIView.as_view()),
    path(route="logout/", view=LogoutAPIView.as_view()),
    path(route="delete/", view=UserDeleteAPIView.as_view()),
]

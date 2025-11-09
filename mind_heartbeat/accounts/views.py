from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class UserRegistrationAPIView(generics.CreateAPIView):
    """User registration view."""

    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                data={
                    "message": "ユーザー登録に成功しました。",
                    "user": UserRegistrationSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """User login view."""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            return Response(
                data={
                    "message": "ログインに成功しました。",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveAPIView):
    """User detail view."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            data={
                "message": "ユーザー情報の取得に成功しました。",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserUpdateAPIView(generics.UpdateAPIView):
    """User update view."""

    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                data={
                    "message": "ユーザー情報の更新に成功しました。",
                    "user": UserUpdateSerializer(instance).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeAPIView(generics.UpdateAPIView):
    """User password change view."""

    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                data={"message": "パスワードの変更に成功しました。"},
                status=status.HTTP_200_OK,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """User logout view."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.session.clear()
        return Response(
            data={"message": "ログアウトに成功しました。"},
            status=status.HTTP_200_OK,
        )


class UserDeleteAPIView(generics.DestroyAPIView):
    """User delete view."""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={"message": "ユーザーの削除に成功しました。"},
            status=status.HTTP_200_OK,
        )

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AbstractUser  # yoki AbstractUser agar shunday nomlangan bo‘lsa
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = AbstractUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": self.get_serializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role  # Bu qatorni qoldirsang JWT token ichida "role" field ham bo‘ladi

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserRegistrationSerializer(user).data,
        }, status=status.HTTP_200_OK)


class UserPasswordChangeView(generics.GenericAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [IsAuthenticated]  # faqat user roli bo‘lsa

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully."})

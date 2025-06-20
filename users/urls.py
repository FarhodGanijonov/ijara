from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserPasswordChangeView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('change-password/', UserPasswordChangeView.as_view(), name='user-change-password'),
]

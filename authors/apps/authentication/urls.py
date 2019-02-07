from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    SocialAuthView
)

app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="specific_user"),
    path('users/', RegistrationAPIView.as_view(), name="register_user"),
    path('users/login/', LoginAPIView.as_view(), name="login_user"),
    path('social/login/', SocialAuthView.as_view(), name='social_auth'),
]

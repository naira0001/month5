from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmAPIView

urlpatterns =  [
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/login/', AuthorizationAPIView.as_view()),
    path('auth/confirm/', ConfirmAPIView.as_view()),
]
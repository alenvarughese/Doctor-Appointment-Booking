from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, logout

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', logout, name='user-logout'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
]

from django.urls import path
from user.apps import UserConfig
from user.views import UserRegistrationView, UserLoginView, UserLogoutView, UserPasswordResetView, verify_account


app_name = UserConfig.name

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<int:user_pk>/', verify_account, name='verify_account'),
    path('password/reset/', UserPasswordResetView.as_view(), name='reset_password'),
]

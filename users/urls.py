from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import RegisterView, ProfileView, NewPasswordView, email_verification
from users.apps import UsersConfig

app_name = UsersConfig.name

# урлы приложения users
urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('reset-pasword/', NewPasswordView.as_view(), name='reset-password')
]
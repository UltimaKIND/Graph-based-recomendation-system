import secrets, string, random
from django.core.mail import send_mail
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy, reverse
from users.models import User
from graph_recsys.models import Prefer
from users.forms import UserRegistrationForm, UserProfileForm, PasswordForm


class RegisterView(CreateView):
    """
    контроллер регистрации пользователя
    """

    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        Prefer.objects.create(user=user)
        user.is_active = True

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileView(UpdateView):
    """
    контроллер редактирования профиля пользователя
    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class NewPasswordView(PasswordResetView):
    """
    контроллер сброса пароля пользователя
    """

    model = User
    form_class = PasswordForm
    template_name = "users/reset_password.html"
    success_url = reverse_lazy("users/login.html")

    def generate_password(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(characters) for _ in range(length))
        return password

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = get_object_or_404(User, email=email)
        password = self.generate_password(16)
        user.set_password(password)
        user.save()
        send_mail(
            subject="вы запросили сброс пароля",
            message=f"новый пароль для входа: {password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return redirect(reverse("users:login"))

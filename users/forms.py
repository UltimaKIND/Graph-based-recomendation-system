from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms
from django.forms import BooleanField

from users.models import User

class StyleFormMixin:
    """
    класс-миксин для стилизации форм
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance (field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"

class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')

class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма профиля пользователя
    """

    class Meta:
        model = User
        fields = ('first_name', 'email', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

class PasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Форма сброса пароля
    """
    class Meta:
        model = User
        fields = ('email',)

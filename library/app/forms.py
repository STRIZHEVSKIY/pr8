from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput,
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class SettingsForm(forms.ModelForm):
    lang = forms.ChoiceField(choices=[('ru', 'Русский'), ('en', 'Английский')], label='Выберите язык')
    theme = forms.ChoiceField(choices=[('light', 'Светлая'), ('dark', 'Темная')], label='Выберите тему')

    class Meta:
        model = User
        fields = ['lang', 'theme']


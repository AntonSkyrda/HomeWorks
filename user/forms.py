from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]

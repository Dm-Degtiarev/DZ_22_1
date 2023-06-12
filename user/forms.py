from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'avatar', 'phone_number', 'country')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'

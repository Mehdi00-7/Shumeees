from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email: forms.EmailField = forms.EmailField(label="Email")
    first_name: forms.CharField = forms.CharField(label="First Name")
    last_name: forms.CharField = forms.CharField(label="Last Name")
    date_of_birth: forms.DateField = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )

    class Meta:
        model: type[User] = User
        fields: tuple[str, ...] = (
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
        )

    def save(self, commit: bool = True) -> User:
        user: User = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        if commit:
            user.save()
        return user

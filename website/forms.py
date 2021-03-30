from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, URLInput, FileInput

from .models import Comment, Post, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password.widget.attrs.update({"class": "formfield"})

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "formfield",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "formfield",
                }
            ),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "website",
            "picture",
        )
        widgets = {
            "website": URLInput(
                attrs={
                    "class": "formfield",
                }
            ),
            "picture": FileInput(
                attrs={
                    "class": "formfield",
                }
            ),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("creator", "time_created", "slug")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = (
            "post",
            "user",
            "time_created",
        )
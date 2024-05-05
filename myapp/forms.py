from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = "__all__"


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = "__all__"


class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = "__all__"


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('name', 'actors', 'user', 'translation', 'year', 'country', 'genre', 'image', 'video', 'free')
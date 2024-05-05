from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",  "first_name", "last_name", "username", "email", "is_staff"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = "__all__"


class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    translation = TranslationSerializer()
    year = YearSerializer()
    country = CountrySerializer()
    free = serializers.BooleanField()
    price = serializers.IntegerField()

    class Meta:
        model = Film
        fields = "__all__"


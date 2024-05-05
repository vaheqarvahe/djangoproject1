from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return f"{self.year}"


class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Translation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=200)
    actors = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='film_images')
    video = models.FileField(upload_to='film_video')
    free = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AcceptPayment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

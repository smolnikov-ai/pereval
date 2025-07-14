from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .resources import (CHOICES_LEVEL_DIFFICULTY_PEREVAL,
                        CHOICES_STATUS_MODERATION_PEREVAL)


class User(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email Address')
    fam = models.CharField(max_length=50, verbose_name="Family Name")
    name = models.CharField(max_length=50, verbose_name="Name")
    otc = models.CharField(max_length=50, blank=True, null=True, verbose_name="Patronymic")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.fam} {self.name} {self.otc or ''}"


class Coords(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude",
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude",
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
    height = models.IntegerField(verbose_name="Height")

    class Meta:
        verbose_name = 'Coordinates'
        verbose_name_plural = 'Coordinates'

    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.height}"


class Level(models.Model):
    winter = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Winter Level",)
    summer = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Summer Level",)
    autumn = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Autumn Level",)
    spring = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Spring Level",)

    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'


class Pereval(models.Model):
    beauty_title = models.CharField(blank=True, null=True,)
    title = models.CharField()
    other_titles = models.CharField(blank=True, null=True,)
    connect = models.CharField()
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(choices=CHOICES_STATUS_MODERATION_PEREVAL, default='new')


class Images(models.Model):
    data = models.URLField()
    title = models.CharField(max_length=50)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name="images")

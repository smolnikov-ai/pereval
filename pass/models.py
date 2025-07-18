from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .resources import (CHOICES_LEVEL_DIFFICULTY_PEREVAL,
                        CHOICES_STATUS_MODERATION_PEREVAL)


class User(models.Model):
    """
    The class models User entity objects in the application

    Attributes:
        email (EmailField): the email of the user
        fam (CharField): user's last name
        name (CharField): user's first name
        otc (CharField): user's patronymic, optional field
        phone (CharField): user's phone number, optional field

    Methods:
        __str__(): returns a string with the user's full name

    Metadata:
        verbose_name (str): used to display a single entity in the admin panel
        verbose_name_plural (str): used to display multiple entities in the admin panel
    """
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
    """
    The class models Coords entity objects in the application

    Attributes:
        latitude (DecimalField): the latitude of the point on the pass
        longitude (DecimalField): the longitude of the point on the pass
        height (IntegerField): the height of the point on the pass

    Methods:
        __str__(): returns a string with the full coordinates

    Metadata:
        verbose_name (str): used to display a single entity in the admin panel
        verbose_name_plural (str): used to display multiple entities in the admin panel
    """
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
    """
    The class models Level entity objects in the application

    Attributes:
        winter (CharField): the difficulty level of the pass in winter
        summer (CharField): the difficulty level of the pass in summer
        autumn (CharField): the difficulty level of the pass in autumn
        spring (CharField): the difficulty level of the pass in spring

    Metadata:
        verbose_name (str): used to display a single entity in the admin panel
        verbose_name_plural (str): used to display multiple entities in the admin panel
    """
    winter = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Winter Level",)
    summer = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Summer Level",)
    autumn = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Autumn Level",)
    spring = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, verbose_name="Spring Level",)

    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'


class Pereval(models.Model):
    """
    The class models Pereval entity objects in the application

    Attributes:
        beauty_title (CharField): the euphonious name of the pass
        title (CharField): the official name of the pass
        other_titles (CharField): alternative names of the pass
        connect (CharField): additional information
        add_time (DateTimeField): time of record creation
        user (ForeignKey): the user who created the record
        coords (ForeignKey): coordinates of the pass
        level (ForeignKey): difficulty level of the pass
        status (CharField): recording status

    """
    beauty_title = models.CharField(blank=True, null=True,)
    title = models.CharField()
    other_titles = models.CharField(blank=True, null=True,)
    connect = models.CharField(blank=True, null=True,)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(choices=CHOICES_STATUS_MODERATION_PEREVAL, default='new')


class Images(models.Model):
    """
    The class models Images entity objects in the application

    Attributes:
        data (URLField): image link
        title (CharField): title of the image
        pereval (ForeignKey): the pass that the image belongs to
    """
    data = models.URLField()
    title = models.CharField(max_length=50)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name="images")

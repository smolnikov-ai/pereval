from email.mime import image

from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization
    """
    class Meta:
        model = User
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization
    """
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization
    """
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization
    """
    class Meta:
        model = Images
        fields = ['data', 'title', ]


class PerevalSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data between a model object and JSON format

    Attributes:
        user(UserSerializer): serializer for the "User" field
        coords(CoordsSerializer): serializer for the "Coords" field
        level(LevelSerializer): serializer for the "Level" field
        images(ImagesSerializer): serializer for the "Images" field

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization

    Methods:
        create: Creating a new Pereval object with the creation of dependent models.
                The method creates a new record in the Pereval table and associates
                it with the User, Coords, Level objects and many photos (Images).
    """
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles',
                  'connect', 'add_time', 'user', 'coords',
                  'level', 'status', 'images', ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(**user_data)
        coords_data = validated_data.pop('coords')
        coords_instance = Coords.objects.create(**coords_data)
        level_data = validated_data.pop('level')
        level_instance = Level.objects.create(**level_data)
        images_data = validated_data.pop('images')

        pereval_instance = Pereval.objects.create(
            user=user_instance, coords=coords_instance,
            level=level_instance, **validated_data, )

        for image in images_data:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(pereval=pereval_instance, data=data, title=title)

        return pereval_instance


class PerevalInfoSerializer(serializers.ModelSerializer):
    """
    A serializer for converting data between a model object and JSON format

    Attributes:
        user(UserSerializer): serializer for the "User" field
        coords(CoordsSerializer): serializer for the "Coords" field
        level(LevelSerializer): serializer for the "Level" field
        images(ImagesSerializer): serializer for the "Images" field

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization
    """
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles',
                  'connect', 'add_time', 'user', 'coords',
                  'level', 'status', 'images', ]


class CoordsUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer for updating data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization

    Methods:
        update: updating data between a model object and JSON format
    """
    class Meta:
        model = Coords
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.altitude = validated_data.get('altitude', instance.altitude)


class LevelUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer for updating data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization

    Methods:
        update: updating data between a model object and JSON format
    """
    class Meta:
        model = Level
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.winter = validated_data.get('winter', instance.winter)
        instance.summer = validated_data.get('summer', instance.summer)
        instance.autumn = validated_data.get('autumn', instance.autumn)
        instance.spring = validated_data.get('spring', instance.spring)


class ImagesUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer for updating data between a model object and JSON format

    Metadata:
        model: the model corresponding to this serializer
        fields: list of model fields included in serialization

    Methods:
        update: updating data between a model object and JSON format
    """
    class Meta:
        model = Images
        fields = ['data', 'title', ]

    def update(self, instance, validated_data):
        instance.data = validated_data.get('images', instance.data)
        instance.title = validated_data.get('title', instance.title)


class PerevalUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer for updating data between a model object and JSON format

    Attributes:
        coords(CoordsSerializer): serializer for the "Coords" field
        level(LevelSerializer): serializer for the "Level" field
        images(ImagesSerializer): serializer for the "Images" field

    Methods:
        update: updating data between a model object and JSON format
    """
    coords = CoordsUpdateSerializer()
    level = LevelUpdateSerializer()
    images = ImagesUpdateSerializer(many=True)

    def update(self, instance, validated_data):
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)

        coords_data = validated_data.pop('coords', None)
        if coords_data is not None:
            LevelUpdateSerializer().update(instance.coords, coords_data)

        level_data = validated_data.pop('level', None)
        if level_data is not None:
            LevelUpdateSerializer().update(instance.level, level_data)

        images_data = validated_data.pop('images', [])
        existing_images = {image.pk: image for image in instance.images.all()}

        for image_data in images_data:
            try:
                pk = int(image_data['pk'])
                existing_image = existing_images[pk]
                ImagesUpdateSerializer().update(existing_image, image_data)
            except KeyError:
                Images.objects.create(pereval=instance, **image_data)

        instance.save()
        return instance


from tkinter import Image

from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coords = CoordsSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    images = ImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Pereval
        fields = '__all__'


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


        for i in images_data:
            data = i.pop('data')
            title = i.pop('title')
            Image.objects.create(pereval=pereval_instance, data=data, title=title)

        return pereval_instance



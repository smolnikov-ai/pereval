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

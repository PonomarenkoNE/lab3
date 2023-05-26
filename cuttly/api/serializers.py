from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from cuttly.settings import HOST
from .models import *


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        return new_user


class URLSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    creator = serializers.SlugRelatedField('username', read_only=True)
    original_url = serializers.CharField(max_length=2048)
    cutted_url = serializers.CharField(read_only=True)

    class Meta:
        model = URL
        fields = ('id', 'creator', 'original_url', 'cutted_url')

    def create(self, validated_data):
        new_url = URL.objects.create(**validated_data)
        new_url.cutted_url = f'{HOST}/{new_url.id}'
        new_url.save()
        return new_url

    def update(self, instance, validated_data):
        instance.original_url = validated_data.get('original_url', instance.original_url)
        instance.save()
        return instance
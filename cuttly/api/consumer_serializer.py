from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    creator = serializers.SlugRelatedField('username', read_only=True)
    original_url = serializers.CharField(max_length=2048)
    cutted_url = serializers.CharField(read_only=True)

    class Meta:
        model = URL
        fields = ('id', 'creator', 'original_url', 'cutted_url')

from rest_framework import serializers

from .models import Message, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['url', 'name', 'content', 'source', 'coordinates', 'problem_type', 'category_type', 'status']

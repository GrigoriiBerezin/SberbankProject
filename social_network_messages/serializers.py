from rest_framework import serializers

from .models import Message, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='coordinates.name')
    problem = serializers.CharField(source='get_problem_type_display')
    category = serializers.CharField(source='get_category_type_display')
    tone = serializers.CharField(source='get_tone_display')
    emotionality = serializers.CharField(source='get_emotionality_display')

    class Meta:
        model = Message
        fields = ['id',
                  'status',
                  'url',
                  'name',
                  'content',
                  'source',
                  'city_name',
                  'problem',
                  'category',
                  'tone',
                  'emotionality',
                  'created_at']

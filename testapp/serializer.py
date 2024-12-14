from rest_framework import serializers
from .models import Room, AirConditioner

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class AirConditionerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirConditioner
        fields = '__all__'
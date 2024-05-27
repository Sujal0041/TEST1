from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(**validated_data)
    #     return user
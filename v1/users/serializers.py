from rest_framework import serializers
from .models import User
from v1.utils.raise_errors import SerializerRaise400


class CustomerRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)
    password1 = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)
    password2 = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        username = validated_attrs['username']
        password1 = validated_attrs['password1']
        password2 = validated_attrs['password2']

        if password1 != password2:
            raise SerializerRaise400("Passwords must match.")

        user = User.objects.filter(username=username).last()
        if user:
            raise SerializerRaise400('Username has already taken.')

        return validated_attrs

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'], password=validated_data['password1'])

    def to_representation(self, instance):
        return {
            "username": instance.username
        }

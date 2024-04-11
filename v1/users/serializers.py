from rest_framework import serializers
from .models import User
from v1.utils.raise_errors import SerializerRaise400


class CustomerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)
    phone_number = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)
    password1 = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)
    password2 = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        phone_number = validated_attrs['phone_number']
        password1 = validated_attrs['password1']
        password2 = validated_attrs['password2']

        if password1 != password2:
            raise SerializerRaise400("Passwords must match.")

        user = User.objects.filter(phone_number=phone_number).last()
        if user:
            raise SerializerRaise400('Phone number has already taken.')

        return validated_attrs

    def create(self, validated_data):
        validated_data.pop('password1')
        validated_data['password'] = validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        return {
            'success': True,
            "phone_number": instance.phone_number
        }

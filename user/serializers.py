from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'password', 
            'confirm_password'
        ]

        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "This email already exists."
            })
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Unable to login',
                )
        else:
            raise serializers.ValidationError("Email and Password are required..")

        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
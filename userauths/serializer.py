from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from userauths.models import User, Profile
from rest_framework.throttling import UserRateThrottle


class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['phone'] = user.phone
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password', 'password_repeat']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_repeat')

        email_username = validated_data['email'].split('@')[0]

        user = User.objects.create_user(
            username=email_username,
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            full_name=validated_data.get('full_name'),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

class PasswordChangeSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True, required=True)
    uidb64 = serializers.CharField(write_only=True, required=True)
    reset_token = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        
        
    )

    def validate_password(self, value):
        user = self.context.get('user')  
        if user and user.check_password(value):
            raise serializers.ValidationError("شما نمیتوانید رمز عبور خود را به رمز فعلی خود تغییر دهید.")
        validate_password(value)
        return value
    

class PasswordResetThrottle(UserRateThrottle):
    rate = '1/m'  
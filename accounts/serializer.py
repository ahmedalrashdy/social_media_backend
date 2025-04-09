
from email.policy import default
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')

class RegisterSerializer(serializers.Serializer):
    name=serializers.CharField(required=False,max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password])

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ConfirmResetSerializer(serializers.Serializer):
    reset_token =  serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(validators=[validate_password])

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
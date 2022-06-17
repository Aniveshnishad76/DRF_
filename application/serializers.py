from rest_framework import serializers

from application.models import UserInfo, UserOTP


class SendOTP(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["mobile_no","email"]
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'id',    'last_login', "is_superuser", "is_staff", "is_active", "date_joined", "password",
            "is_verified",
            "groups", "user_permissions")


# class OTP(serializers.ModelSerializer):
#     class Meta:
#         model = UserOTP
#         fields = ["user", "otp"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}


class ActionsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'email', 'mobile_no', 'profile', "is_premium", "location", 'business_type',
                  "is_partner", 'id', 'email', 'last_login', "is_superuser", "is_staff", "is_active", "date_joined",
                  "is_verified"]
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'id', 'email', 'last_login', "is_superuser", "is_staff", "is_active", "date_joined", "password",
            "is_verified",
            "groups", "user_permissions")


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['password']
        read_only_fields = (
            'id', 'email', 'last_login', "is_superuser", "is_staff", "is_active", "date_joined",
            "is_verified", "is_partner",
            "groups", "user_permissions", 'first_name', 'last_name', 'mobile_no')

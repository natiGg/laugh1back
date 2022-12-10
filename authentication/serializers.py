from dataclasses import field
import profile
from pyexpat import model
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db.models import fields
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from authentication.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from core.models import UserProfile
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name','phone_number','bod','gender','profile_pic')

class UserRegisteration(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ['id','email','username','password']
    def validate(self, attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError("The username should only contain alpahnumeric character")
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) 
        UserProfile.objects.create(
            user=user,
        )
        return user

class UpdateProfileSerializer(serializers.ModelSerializer):

  
    class Meta:
        model = UserProfile
        fields = ["user","name","phone_number","bod","gender","profile_pic"]

    def save(self, *args, **kwargs):
        if self.instance.profile_pic:
            self.instance.profile_pic.delete()
        return super().save(*args, **kwargs)

class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user","profile_pic"]

    def save(self, *args, **kwargs):
        if self.instance.profile_pic:
            self.instance.profile_pic.delete()
        return super().save(*args, **kwargs)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)
    class Meta:
        model=User
        fields=['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=1)
    password=serializers.CharField(max_length=68,min_length=8,write_only=True)
    # id = serializers.IntegerField(read_only=True)
    # username = serializers.EmailField(max_length=255,min_length=1,read_only=True)
    tokens=serializers.CharField(max_length=68,min_length=8,read_only=True)
    
    class Meta:
        model=User
        fields=['email','password','tokens']
    
    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','') 
        user=auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")  
        if not user.is_active:
            raise AuthenticationFailed("Account, try again")
        if not user.is_verified:
            raise AuthenticationFailed("email is not verified, try again")
        
        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens
        }

    
class PasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    redirect_url=serializers.CharField(max_length=500,required=False)
    class Meta:
        fields = ['email']


class ChangePwdSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6,max_length=68,write_only=True)
    token=serializers.CharField(min_length=1,write_only=True)
    uidb64=serializers.CharField(min_length=1,write_only=True)
    class Meta:
        fields=['password','token','uidb64'] 
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid',401)

class EmailCheckSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255,min_length=1)
        class Meta:
            fields=["email"]

class UnameCheckSerializer(serializers.Serializer):
        username = serializers.EmailField(max_length=255,min_length=1)
        class Meta:
            fields=["username"]
            
class UnameSuggestSerializer(serializers.Serializer):
        username = serializers.EmailField(max_length=255,min_length=1)
        class Meta:
            fields=["username"]

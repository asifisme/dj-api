from rest_framework import serializers 
from django.contrib.auth import get_user_model 
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.password_validation import validate_password 


User = get_user_model() 


class SingUpSerializer(serializers.ModelSerializer):
    """ """

    confirm_password = serializers.CharField(write_only=True)
    password         = serializers.CharField(write_only=True, required=True)
    username         = serializers.CharField(required=True, max_length=150) 
    phn_num          = serializers.CharField(required=True, max_length=15)

    class Meta:
        model       = User 
        fields      = ['first_name', 'last_name', 'email', 'phn_num', 'username', 'password', 'confirm_password']

    def validate(self, attrs):
        """ password validation """ 
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        return super().validate(attrs)
    
    def validate_username_and_email(self, attrs):
        """ username and email validation """
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})
        return super().validate(attrs) 
    
    def vaildate_phn_num(self, attrs):
        """ phone number validation """
        if User.objects.filter(phn_num=attrs['phn_num']).exists():
            raise serializers.ValidationError({'phn_num': 'Phone number already exists.'})
        return super().validate(attrs)  
    

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    

class SignInSerializer(serializers.Serializer):
    """ sign in serializer """
    username_or_email   = serializers.CharField(required=True)
    password            = serializers.CharField(required=True, write_only=True)
    # remember_me        = serializers.BooleanField(default=False, required=False)

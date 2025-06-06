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

    class Meta:
        model       = User 
        fields      = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']

    def validate(self, attrs):
        """ password validation """ 
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        return super().validate(attrs)
    
    def validate__email(self, value):
        """ email validation """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        return value 
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})
        return value
    
    
    
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




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        return attrs 
    



class ResetPasswordRequestSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True) 

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')

        if not username_or_email or not username_or_email.strip():
            raise serializers.ValidationError('Username or email is required') 
        
        return attrs 
    



class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match.'})
        return attrs



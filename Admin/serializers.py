from rest_framework import serializers 
from django.contrib.auth import get_user_model 

from .models import MailTable 

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model      = User 
        fields     =  "__all__" 



class MaiTablelSerializer(serializers.ModelSerializer):
    class Meta:
        model   = MailTable 
        fields  = "__all__"
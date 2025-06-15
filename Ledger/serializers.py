from rest_framework import serializers 


class TrialBalanceSerializer(serializers.Serializer):
    created = serializers.DateField(required=True) 
    ended = serializers.DateField(required=True)


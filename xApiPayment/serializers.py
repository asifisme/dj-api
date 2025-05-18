from rest_framework import serializers 


from .models import PaymentModel 


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentModel
    """
    class Meta:
        model = PaymentModel
        fields = '__all__'
        read_only_fields = ('created', 'modified', 'order', 'user')
    

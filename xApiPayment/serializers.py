from rest_framework import serializers 


from .models import PaymentModel 
from xApiCart.models import OrderModel 


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentModel
    """
    class Meta:
        model = PaymentModel
        fields = '__all__'
        read_only_fields = ('created', 'modified', 'order', 'user')
    

class PaymentSerializerForPayment(serializers.ModelSerializer):
    """ Serializer for PaymentModel for payment processing """
    class Meta:
        model = OrderModel 
        fields = "__all__"
        # read_only_fields = ('created', 'modified', 'order', 'user')


class OrderPaymentProcessorSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderModel
    """
    confirm  = serializers.BooleanField(default=False) 
    
    class Meta:
        model = OrderModel 
        fields = ['id', 'total_amount', 'confirm' ]
        # fields = '__all__'

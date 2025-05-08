from rest_framework import serializers 


from xApiProduct.models import ProductCategoryModel 
from xApiProduct.models import ProductMetaTagModel
from xApiProduct.models import ProductModel
from xApiProduct.models import ProductImageModel


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product categories.
    """
    class Meta:
        model = ProductCategoryModel
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified']

        


class ProductMetaTagSerializer(serializers.ModelSerializer):
    """
    Serializer for product meta tags.
    """
    class Meta:
        model = ProductMetaTagModel
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified']



class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products.
    """
    class Meta:
        model = ProductModel
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified'] 



class ProductImageSerializer(serializers.ModelSerializer):
    """ 
    Serializer for product images.
    """

    class Meta:
        model = ProductImageModel
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified']
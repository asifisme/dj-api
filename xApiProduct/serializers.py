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




# for only send data... 

class ProductImageSerializer(serializers.ModelSerializer):
    """ 
    Serializer for product images.
    """

    class Meta:
        model = ProductImageModel
        fields =  ['image'] #['id', 'image', 'author', 'created', 'modified']
        read_only_fields = ['id', 'created', 'modified']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products.
    """
    images = ProductImageSerializer(many=True, read_only=True) 
    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'title', 'desc', 'price', 'stock','slug', 'uid', 'images']  # '__all__'
        read_only_fields = ['id', 'created', 'modified', ] 
        #exclude = ['created', 'modified', 'unq_num',]
        # 




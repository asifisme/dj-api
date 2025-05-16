from rest_framework import serializers 


from .models import ProductCategoryModel 
from .models import ProductMetaTagModel
from .models import ProductModel
from .models import ProductImageModel


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product categories.
    """
    class Meta:
        model = ProductCategoryModel
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified']

    
    def validate(self, attrs):
        if not attrs.get('cate_name') or not str(attrs.get('cate_name').strip()):
            raise serializers.ValidationError('Category is required')
        # if not attrs.get('slug') or not str(attrs.get('slug').strip()):
        #     raise serializers.ValidationError('Slug must required')
        return super().validate(attrs)

    

        


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
        #exclude = ['created', 'modified', 'unq_num',



class data(serializers.Serializer):
    pass 

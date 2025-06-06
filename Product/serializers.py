from rest_framework import serializers 


from .models import ProductCategoryModel 
from .models import ProductMetaTagModel
from .models import ProductModel
from .models import WishListProduct 
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
        fields =  ['id', 'product', 'author', 'product_image', 'is_primary', 'alt_text']
        read_only_fields = ['id', 'created', 'modified']




class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = ProductModel
        fields = '__all__' 
        # fields = [
        #     'id', 'category', 'author', 'meta_tag', 'name', 'title', 'slug', 'description', 'weight', 'sku',
        #     'price', 'discount_percent', 'stock', 'warranty_information', 'shipping_information', 'return_policy',
        #     'min_order_quantity', 'unq_num', 'pro_uuid', 'is_available', 'is_approved', 'rating', 'views_count',
        #     'sold_count', 'uid', 'images', 'created', 'modified'
        # ]
        read_only_fields = ['id', 'created', 'modified', 'unq_num', 'pro_uuid', 'uid', 'images']





class WishListProductSerializer(serializers.ModelSerializer):
    """
    Serializer for wishlist products.
    """
    class Meta:
        model = WishListProduct
        fields = '__all__'
        read_only_fields = ['id', 'added_at']
    
    def validate(self, attrs):
        if not attrs.get('product'):
            raise serializers.ValidationError('Product is required')
        if not attrs.get('user'):
            raise serializers.ValidationError('User is required')
        return super().validate(attrs)
    
    def duplicate_product_check(self, attrs):
        """
        Check if the product is already in the user's wishlist.
        """
        user = attrs.get('user')
        product = attrs.get('product')
        if WishListProduct.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError('This product is already in your wishlist.')
        return attrs
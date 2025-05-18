from rest_framework import serializers 


from .models import ArticleCategoryModel 
from .models import ArticleMetaTag 
from .models import ArticleModel 
from .models import ArticleImageModel 


class ArticleCategorySerializer(serializers.ModelSerializer):
    """ Serializer for Article Category Model """
    
    class Meta:
        model = ArticleCategoryModel
        fields = '__all__'
        read_only_fields = ('uid', 'created', 'modified')
        # extra_kwargs = {
        #     'author': {'required': False, 'allow_null': True}
        # } 




class ArticleMetaTagSerializer(serializers.ModelSerializer):
    """ Serializer for Article Meta Tag Model """
    
    class Meta:
        model = ArticleMetaTag
        fields = '__all__'
        read_only_fields = ('uid', 'created', 'modified')
        # extra_kwargs = {
        #     'author': {'required': False, 'allow_null': True}
        # } 




class ArticleSerializer(serializers.ModelSerializer):
    """ Serializer for Article Model """
    
    class Meta:
        model = ArticleModel
        fields = '__all__'
        read_only_fields = ('uid', 'created', 'modified')
        # extra_kwargs = {
        #     'author': {'required': False, 'allow_null': True},
        #     'cate_id': {'required': False, 'allow_null': True}
        # } 




class ArticleImageSerializer(serializers.ModelSerializer):
    """ Serializer for Article Image Model """
    
    class Meta:
        model = ArticleImageModel
        fields = '__all__'
        read_only_fields = ('uid', 'created', 'modified')
        # extra_kwargs = {
        #     'author': {'required': False, 'allow_null': True},
        #     'article': {'required': False, 'allow_null': True}
        # } 
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
      



class ArticleMetaTagSerializer(serializers.ModelSerializer):
    """ Serializer for Article Meta Tag Model """
    
    class Meta:
        model = ArticleMetaTag
        fields = '__all__'
        read_only_fields = ('uid', 'created', 'modified')
     


class ArticleImageSerializer(serializers.ModelSerializer):
    """ Serializer for Article Image Model """
    
    class Meta:
        model = ArticleImageModel
        fields = ['id', 'image', 'alt_text']
    



class ArticleSerializer(serializers.ModelSerializer):
    """ Serializer for Article Model """

    images = ArticleImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ArticleModel
        fields = '__all__'
        read_only_fields = ('uid', 'images', 'created', 'modified')
     
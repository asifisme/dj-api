from rest_framework import viewsets 
from rest_framework import permissions 
from rest_framework.exceptions import ValidationError 
from rest_framework import throttling 

from .models import ArticleCategoryModel 
from .models import ArticleMetaTag 
from .models import ArticleModel 
from .models import ArticleImageModel 


from .serializers import ArticleCategorySerializer 
from .serializers import ArticleMetaTagSerializer 
from .serializers import ArticleSerializer 
from .serializers import ArticleImageSerializer 




class ArticleCategoryViewSet(viewsets.ModelViewSet): 
    """ ViewSet for Article Category """
    queryset                  = ArticleCategoryModel.objects.all()
    serializer_class          = ArticleCategorySerializer
    permission_classes        = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names         = ['get', 'post', 'put', 'delete'] 
    throttle_classes          = [throttling.UserRateThrottle]
    # lookup_field = 'uid'

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user) 
        except Exception as e:
            raise ValidationError(f"Error creating Article Category: {str(e)}") 




class ArticleMetaTagViewSet(viewsets.ModelViewSet): 
    """ ViewSet for Article Meta Tag """
    queryset                  = ArticleMetaTag.objects.all()
    serializer_class          = ArticleMetaTagSerializer
    permission_classes        = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names         = ['get', 'post', 'put', 'delete'] 
    throttle_classes          = [throttling.UserRateThrottle]
    # lookup_field = 'uid'
    
    def perform_create(self, serializer):
       try:
            serializer.save(author=self.request.user)
       except Exception as e:
            raise ValidationError(f"Error creating Article Meta Tag: {str(e)}")




class ArticleViewSet(viewsets.ModelViewSet):
    """ ViewSet for Article """
    queryset                  = ArticleModel.objects.all()
    serializer_class          = ArticleSerializer
    http_method_names         = ['get', 'post', 'put', 'delete'] 
    permission_classes        = [permissions.AllowAny]
    throttle_classes          = [throttling.UserRateThrottle]
    # lookup_field = 'uid'
    
    def perform_create(self, serializer):
       try:
            serializer.save(author=self.request.user)
       except Exception as e:
            raise ValidationError(f"Error creating Article: {str(e)}")




class ArticleImageViewSet(viewsets.ModelViewSet):
    """ ViewSet for Article Image """
    queryset                  = ArticleImageModel.objects.all()
    serializer_class          = ArticleImageSerializer
    http_method_names         = ['get', 'post', 'put', 'delete'] 
    permission_classes        = [permissions.AllowAny]
    throttle_classes          = [throttling.UserRateThrottle]
#     lookup_field = 'uid'
    
    def perform_create(self, serializer):
       try:
            serializer.save(author=self.request.user)
       except Exception as e:
            raise ValidationError(f"Error creating Article Image: {str(e)}")

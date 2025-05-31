from rest_framework import viewsets 
from rest_framework import permissions 
from rest_framework.exceptions import ValidationError 
from rest_framework import throttling 
from rest_framework import filters 

from .models import ArticleCategoryModel 
from .models import ArticleMetaTag 
from .models import ArticleModel 
from .models import ArticleImageModel 


from .serializers import ArticleCategorySerializer 
from .serializers import ArticleMetaTagSerializer 
from .serializers import ArticleSerializer 
from .serializers import ArticleImageSerializer 

from core.core_permissions import IsOwnerOrReadOnly
from core.xpagepagination import DynamicPagination  



class ArticleCategoryViewSet(viewsets.ModelViewSet): 
    """ ViewSet for Article Category """
    queryset                  = ArticleCategoryModel.objects.all()
    serializer_class          = ArticleCategorySerializer
    permission_classes        = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names         = ['get', 'post', 'delete'] 
    pagination_class          = DynamicPagination 
    filter_backends           = [filters.SearchFilter]
    search_fields             = ['cate_name', 'uid'] 
    throttle_classes          = [throttling.UserRateThrottle]
    # lookup_field = 'uid'

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user) 
        except Exception as e:
            raise ValidationError(f"Error creating Article Category: {str(e)}") 
        
    def get_queryset(self):
        """Override to customize the queryset."""
        uid = self.request.query_params.get('q', None) 
        if uid:
            return self.queryset.filter(uid=uid) 
        return super().get_queryset()




class ArticleMetaTagViewSet(viewsets.ModelViewSet): 
    """ ViewSet for Article Meta Tag """
    queryset                  = ArticleMetaTag.objects.all()
    serializer_class          = ArticleMetaTagSerializer
    permission_classes        = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names         = ['get', 'post', 'delete'] 
    filter_backends           = [filters.SearchFilter]
    search_fields             = ['tag', 'meta_title', 'meta_keywords', 'uid']  
    pagination_class          = DynamicPagination 
    throttle_classes          = [throttling.UserRateThrottle]
    
    def perform_create(self, serializer):
       try:
            serializer.save(author=self.request.user)
       except Exception as e:
            raise ValidationError(f"Error creating Article Meta Tag: {str(e)}")

    def get_queryset(self):
        """Override to customize the queryset."""
        uid = self.request.query_params.get('q', None) 
        if uid:
            return self.queryset.filter(uid=uid) 
        return super().get_queryset()




class ArticleViewSet(viewsets.ModelViewSet):
    """ ViewSet for Article """
    queryset                  = ArticleModel.objects.all()
    serializer_class          = ArticleSerializer
    http_method_names         = ['get', 'post', 'delete'] 
    permission_classes        = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class          = DynamicPagination
    filter_backends           = [filters.SearchFilter]
    search_fields             = ['title', 'slug', 'description', 'summary', 'uid']
    throttle_classes          = [throttling.UserRateThrottle]
    # lookup_field = 'uid'
    
    def perform_create(self, serializer):
       try:
            serializer.save(author=self.request.user)
       except Exception as e:
            raise ValidationError(f"Error creating Article: {str(e)}")
       
    def get_queryset(self):
        uid = self.request.query_params.get('q', None)
        if uid:
            return self.queryset.filter(uid=uid)
        return super().get_queryset() 




class ArticleImageViewSet(viewsets.ModelViewSet):
    """ ViewSet for Article Image """
    queryset                  = ArticleImageModel.objects.all()
    serializer_class          = ArticleImageSerializer
    http_method_names         = ['get', 'post', 'delete'] 
    permission_classes        = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    throttle_classes          = [throttling.UserRateThrottle]
#     lookup_field = 'uid'
    
    def perform_create(self, serializer):
       try:
            serializer.save(author=self.request.user)
       except Exception as e:
            raise ValidationError(f"Error creating Article Image: {str(e)}")

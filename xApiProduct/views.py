import logging 
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import permissions 
from rest_framework import filters
from rest_framework import throttling  



from .models import ProductCategoryModel
from .models import ProductMetaTagModel
from .models import ProductModel
from .models import ProductImageModel 


from .serializers import ProductCategorySerializer
from .serializers import ProductMetaTagSerializer
from .serializers import ProductSerializer
from .serializers import ProductImageSerializer 

from core.xpagepagination import DynamicPagination
from core.core_permissions import IsOwnerOrReadOnly 
from core.core_permissions import IsOwnerStaffOrSuperUser 



logger = logging.getLogger(__name__) 


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product categories.
    """
    queryset               = ProductCategoryModel.objects.all()
    serializer_class       = ProductCategorySerializer
    permission_classes     = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names      = ['get', 'post', 'delete']
    pagination_class       = DynamicPagination
    filter_backends        = [filters.SearchFilter] 
    search_fields          = ['slug', 'cate_name', 'cate_desc', 'uid'] 
    throttle_classes       = [throttling.UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
        return super().perform_create(serializer)
    
    def get_queryset(self):
        """Override to customize the queryset."""
        uid = self.request.query_params.get('q', None) 
        if uid:
            return self.queryset.filter(uid=uid) 
        return super().get_queryset() 






class ProductMetaTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product meta tags.
    """
    queryset                = ProductMetaTagModel.objects.all()
    serializer_class        = ProductMetaTagSerializer
    permission_classes      = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names       = ['get', 'post',  'delete']  
    filter_backends        = [filters.SearchFilter] 
    search_fields          = ['tag', 'meta_title', 'meta_desc', 'meta_keywds', 'uid'] 
    pagination_class        = DynamicPagination 
    throttle_classes        = [throttling.UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  
        return super().perform_create(serializer)
    

    def get_queryset(self):
        """Override to customize the queryset.""" 
        uid = self.request.query_params.get('q', None) 
        if uid:
            return self.queryset.filter(uid=uid) 
        return super().get_queryset()




class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products.
    """
    queryset            = ProductModel.objects.all()
    serializer_class    = ProductSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly, IsOwnerStaffOrSuperUser]
    http_method_names   = ['get', 'post', 'delete']  
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['slug', 'title', 'name', 'description', 'uid' ]
    pagination_class    = DynamicPagination 
    throttle_classes    = [throttling.UserRateThrottle]

    def perform_create(self, serializer):
        """Override to set the author to the current user."""
        serializer.save(author=self.request.user) 
        return super().perform_create(serializer) 

    def get_queryset(self):
        """Override to customize the queryset."""
        uid     = self.request.query_params.get('q', None) 
        if uid:
            return self.queryset.filter(uid=uid)
        
        return super().get_queryset()




class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product images.
    """
    queryset                = ProductImageModel.objects.all()
    serializer_class        = ProductImageSerializer
    permission_classes      = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names       = ['get', 'post', 'put', 'delete'] 
    pagination_class        = DynamicPagination 
    throttle_classes        = [throttling.UserRateThrottle]


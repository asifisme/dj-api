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

from common.xpagepagination import DynamicPagination




class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product categories.
    """
    queryset               = ProductCategoryModel.objects.all()
    serializer_class       = ProductCategorySerializer
    permission_classes     = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names      = ['get', 'post', 'put', 'delete']
    pagination_class       = DynamicPagination
    throttle_classes       = [throttling.UserRateThrottle]




class ProductMetaTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product meta tags.
    """
    queryset                = ProductMetaTagModel.objects.all()
    serializer_class        = ProductMetaTagSerializer
    permission_classes      = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names       = ['get', 'post', 'put', 'delete']  
    pagination_class        = DynamicPagination 
    throttle_classes        = [throttling.UserRateThrottle]




class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products.
    """
    queryset            = ProductModel.objects.all()
    serializer_class    = ProductSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names   = ['get', 'post', 'put', 'delete']  
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['slug', 'title', 'name', 'desc', 'uid' ]
    pagination_class    = DynamicPagination 
    throttle_classes    = [throttling.UserRateThrottle]

    def get_queryset(self):
        """Override to customize the queryset."""
        uid     = self.request.query_params.get('q', None) 
        if uid:
            return self.queryset.filter(uid=uid)
        
        return super().get_queryset()




class TopSellingProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for top-selling products.
    """
    queryset                = ProductModel.objects.all()[:1] 
    serializer_class        = ProductSerializer
    permission_classes      = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names       = ['get']
    throttle_classes        = [throttling.UserRateThrottle]




class NewArrivalProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for new arrival products.
    """
    queryset                = ProductModel.objects.all()[:3] 
    serializer_class        = ProductSerializer
    permission_classes      = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names       = ['get'] 
    throttle_classes        = [throttling.UserRateThrottle]
    


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
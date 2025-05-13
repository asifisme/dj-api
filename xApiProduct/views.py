from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import permissions 
from rest_framework import filters


from xApiProduct.models import ProductCategoryModel
from xApiProduct.models import ProductMetaTagModel
from xApiProduct.models import ProductModel
from xApiProduct.models import ProductImageModel 


from xApiProduct.serializers import ProductCategorySerializer
from xApiProduct.serializers import ProductMetaTagSerializer
from xApiProduct.serializers import ProductSerializer
from xApiProduct.serializers import ProductImageSerializer 

from xApiProduct.paginations import StandardResultsSetPagination 


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product categories.
    """
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = StandardResultsSetPagination


class ProductMetaTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product meta tags.
    """
    queryset = ProductMetaTagModel.objects.all()
    serializer_class = ProductMetaTagSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']  
    pagination_class = StandardResultsSetPagination 

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products.
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'put'] #['get', 'post', 'put', 'delete']  
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['slug', 'title', 'name', 'desc', 'uid' ]
    pagination_class = StandardResultsSetPagination 

    # def get_queryset(self):
    #     """Override to customize the queryset."""
    #     slug = self.request.query_params.get('q', None) 
    #     if slug:
    #         return self.queryset.filter(slug=slug)
    #     return super().get_queryset()


class TopSellingProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for top-selling products.
    """
    queryset = ProductModel.objects.all()[:1] 
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']

class NewArrivalProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for new arrival products.
    """
    queryset = ProductModel.objects.all()[:3] 
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get'] 
    
    

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product images.
    """
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 
    pagination_class = StandardResultsSetPagination 
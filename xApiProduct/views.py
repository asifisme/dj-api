from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import permissions 


from xApiProduct.models import ProductCategoryModel
from xApiProduct.models import ProductMetaTagModel
from xApiProduct.models import ProductModel
from xApiProduct.models import ProductImageModel 


from xApiProduct.serializers import ProductCategorySerializer
from xApiProduct.serializers import ProductMetaTagSerializer
from xApiProduct.serializers import ProductSerializer
from xApiProduct.serializers import ProductImageSerializer 


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product categories.
    """
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']


class ProductMetaTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product meta tags.
    """
    queryset = ProductMetaTagModel.objects.all()
    serializer_class = ProductMetaTagSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for products.
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product images.
    """
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete'] 
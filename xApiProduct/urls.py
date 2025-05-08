from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from xApiProduct.views import ProductCategoryViewSet 
from xApiProduct.views import ProductMetaTagViewSet
from xApiProduct.views import ProductViewSet
from xApiProduct.views import ProductImageViewSet 

router = DefaultRouter() 

router.register(r'product-category', ProductCategoryViewSet, basename='product-category')
router.register(r'product-meta-tag', ProductMetaTagViewSet, basename='product-meta-tag')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product-image', ProductImageViewSet, basename='product-image')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from .views import ProductCategoryViewSet 
from .views import ProductMetaTagViewSet
from .views import ProductViewSet
from .views import ProductImageViewSet 



router = DefaultRouter() 

router.register(r'product-category', ProductCategoryViewSet, basename='product-category')
router.register(r'product-meta-tag', ProductMetaTagViewSet, basename='product-meta-tag')
router.register(r'product-image', ProductImageViewSet, basename='product-image')

# product 
router.register(r'product', ProductViewSet, basename='product')
 
urlpatterns = [
    path('', include(router.urls)),
]

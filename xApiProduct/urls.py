from django.urls import path, include 
from rest_framework.routers import DefaultRouter 

from .views import ProductCategoryViewSet 
from .views import ProductMetaTagViewSet
from .views import ProductViewSet
from .views import ProductImageViewSet 
from .views import TopSellingProductViewSet 
from .views import NewArrivalProductViewSet 



router = DefaultRouter() 

router.register(r'product-category', ProductCategoryViewSet, basename='product-category')
router.register(r'product-meta-tag', ProductMetaTagViewSet, basename='product-meta-tag')
router.register(r'product-image', ProductImageViewSet, basename='product-image')

# product 
router.register(r'product', ProductViewSet, basename='product')
router.register(r'top-selling-product', TopSellingProductViewSet, basename='top-selling-product')
#   ViewSet for new arrival products.
router.register(r'new-arrival-product', NewArrivalProductViewSet, basename='new-arrival-product')
 
urlpatterns = [
    path('', include(router.urls)),
]

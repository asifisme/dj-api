from django.urls import path, include 
from rest_framework.routers import DefaultRouter 


from .views import ArticleCategoryViewSet 
from .views import ArticleMetaTagViewSet     
from .views import ArticleViewSet 
from .views import ArticleImageViewSet 

router = DefaultRouter() 
router.register(r'art-categories', ArticleCategoryViewSet, basename='article-category')
router.register(r'art-metatags', ArticleMetaTagViewSet, basename='article-metatag')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'art-images', ArticleImageViewSet, basename='article-image')



urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticatedOrReadOnly 



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
    queryset = ArticleCategoryModel.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 


class ArticleMetaTagViewSet(viewsets.ModelViewSet): 
    """ ViewSet for Article Meta Tag """
    queryset = ArticleMetaTag.objects.all()
    serializer_class = ArticleMetaTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

class ArticleViewSet(viewsets.ModelViewSet):
    """ ViewSet for Article """
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

class ArticleImageViewSet(viewsets.ModelViewSet):
    """ ViewSet for Article Image """
    queryset = ArticleImageModel.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
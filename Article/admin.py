from django.contrib import admin


from .models import ArticleCategoryModel 
from .models import ArticleMetaTag 
from .models import ArticleModel 
from .models import ArticleImageModel 



@admin.register(ArticleCategoryModel)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('cate_name', 'author', 'is_active', 'uid', 'created', 'modified')
    search_fields = ('cate_name', 'author__email')
    list_filter = ('is_active',)
    ordering = ('-created',) 




@admin.register(ArticleMetaTag)
class ArticleMetaTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'meta_title', 'meta_desc', 'meta_robots', 'is_active', 'author', 'uid', 'created', 'modified')
    search_fields = ('tag', 'meta_title', 'author__email')
    list_filter = ('is_active',)
    ordering = ('-created',) 




@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'uid', 'created', 'modified')
    search_fields = ('title', 'author__email')
    list_filter = ('is_active',)
    ordering = ('-created',) 




@admin.register(ArticleImageModel)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'article', 'uid', 'created', 'modified')
    ordering = ('-created',)
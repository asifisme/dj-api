from django.contrib import admin

from xApiProduct.models import ProductCategoryModel 
from xApiProduct.models import ProductMetaTagModel
from xApiProduct.models import ProductModel
from xApiProduct.models import ProductImageModel 

@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductCategoryModel
    """
    list_display = ('cate_name', 'slug', 'author', 'created', 'modified')
    search_fields = ('cate_name', 'slug')
    prepopulated_fields = {'slug': ('cate_name',)}
    list_filter = ('author',)
    ordering = ('-created',) 

@admin.register(ProductMetaTagModel)
class ProductMetaTagAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductMetaTagModel
    """
    list_display = ('tag', 'meta_title', 'meta_keywds', 'author', 'created', 'modified')
    search_fields = ('tag', 'meta_title')
    list_filter = ('author',)
    ordering = ('-created',) 

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductModel
    """
    list_display = ('name', 'title', 'slug', 'price', 'author', 'created', 'modified')
    search_fields = ('name', 'title', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('author',)
    ordering = ('-created',) 


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductImageModel
    """
    list_display = ( 'image', 'created', 'modified')
    search_fields = ('product__name',)
    ordering = ('-created',)
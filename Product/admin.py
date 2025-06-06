from django.contrib import admin

from .models import ProductCategoryModel 
from .models import ProductMetaTagModel
from .models import ProductModel
from .models import WishListProduct 
from .models import ProductImageModel 

@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductCategoryModel
    """
    list_display = ('id', 'cate_name', 'slug', 'author', 'created', 'modified')
    search_fields = ('cate_name', 'slug')
    prepopulated_fields = {'slug': ('cate_name',)}
    list_filter = ('author',)

@admin.register(ProductMetaTagModel)
class ProductMetaTagAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductMetaTagModel
    """
    list_display = ('id','tag', 'meta_title', 'meta_keywds', 'created', 'modified')
    search_fields = ('tag', 'meta_title')

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductModel
    """
    list_display = ('id', 'name', 'title', 'slug', 'price', 'stock', 'author', 'created', 'modified')
    search_fields = ('name', 'title', 'slug', 'sku')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(WishListProduct)
class WishListProductAdmin(admin.ModelAdmin):
    """
    Admin interface for WishListProduct
    """
    list_display = ('id', 'product', 'user', 'added_at')
    search_fields = ('product__name', 'product__title', 'user__username')
    list_filter = ('user',) 



    

@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductImageModel
    """
    list_display = ('product', 'product_image', 'created', 'modified')
    search_fields = ('product__name', 'product__title', 'product__sku')

from django.contrib import admin

from xApiAuthentication.models import CustomUser 

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Custom user admin for the CustomUser model
    """
    list_display = ('email', 'first_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('id', 'email', 'first_name',)
    ordering = ('-date_joined',)
from django.contrib import admin

from .models import MailTable 

@admin.register(MailTable)
class MailTableAdmin(admin.ModelAdmin):
    list_display    = ['author', 'status', 'created', 'subject']
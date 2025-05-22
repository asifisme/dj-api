from django.contrib import admin


from .models import JournalEntryModel  



@admin.register(JournalEntryModel) 
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['ent_name', 'ent_num', 'status', 'author', 'ended']
    list_filter = ['status', 'author'] 
    search_fields = ['ent_name', 'ent_num'] 

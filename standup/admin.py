from django.contrib import admin
from .models import StandupEntry

@admin.register(StandupEntry)
class StandupEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'created_at', 'has_blockers']
    list_filter = ['date', 'user']
    search_fields = ['user__username', 'did', 'doing', 'blockers']

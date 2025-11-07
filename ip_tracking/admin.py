from django.contrib import admin
from .models import RequestLog, BlockedIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'timestamp', 'path']
    search_fields = ['ip_address', 'path']
    readonly_fields = ['timestamp']

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'blocked_at', 'reason']
    search_fields = ['ip_address']
    readonly_fields = ['blocked_at']
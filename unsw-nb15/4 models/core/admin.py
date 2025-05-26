from django.contrib import admin
from .models import TrafficLog

@admin.register(TrafficLog)
class TrafficLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'attack_type', 'blocked')
    list_filter = ('attack_type', 'blocked', 'timestamp')
    search_fields = ('ip_address', 'attack_type')
    ordering = ('-timestamp',)

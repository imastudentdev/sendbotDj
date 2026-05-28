from django.contrib import admin
from .models import SiteConfig

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('bot_token', 'chat_id', 'is_active')
    fields = ('bot_token', 'chat_id', 'is_active')
    
    def has_add_permission(self, request):
        # Faqat bitta konfiguratsiya bo'lishi uchun
        if self.model.objects.count() >= 1:
            return False
        return True
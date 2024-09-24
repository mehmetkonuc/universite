from django.contrib import admin
from .models import SiteSettingsModel

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    
admin.site.register(SiteSettingsModel, SiteSettingsAdmin)

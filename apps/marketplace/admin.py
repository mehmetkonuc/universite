from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.marketplace.models import Category, MarketPlaceModel

admin.site.register(Category, DraggableMPTTAdmin)

@admin.register(MarketPlaceModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'create_at', 'category')
    search_fields = ('title', 'description')
    list_filter = ('create_at', 'category')
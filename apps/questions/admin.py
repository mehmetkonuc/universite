from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.questions.models import Category, QuestionsModel

admin.site.register(Category, DraggableMPTTAdmin)

@admin.register(QuestionsModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'create_at', 'category')
    search_fields = ('title', 'content')
    list_filter = ('create_at', 'category')
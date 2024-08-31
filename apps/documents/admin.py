from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.documents.models import DocumentsModel, DocumentsFolderModel

# admin.site.register(FolderModel, DraggableMPTTAdmin)
admin.site.register(DocumentsModel)
admin.site.register(DocumentsFolderModel)


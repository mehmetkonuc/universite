from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.documents.models import FolderModel, DocumentsModel

admin.site.register(FolderModel, DraggableMPTTAdmin)
admin.site.register(DocumentsModel)


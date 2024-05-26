from django.contrib import admin

# Register your models here.

from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    search_fields = ('user__username', 'file')

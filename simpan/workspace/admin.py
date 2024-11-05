from django.contrib import admin
from django.http import HttpRequest
from django.db.models import JSONField
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget
from workspace.models import *


@admin.register(StudioStorage)
class StudioStorageAdmin(admin.ModelAdmin):

    model = StudioStorage
    list_display = ("id", "file", "created_at", "updated_at")
    search_fields = ("file",)
    list_filter = ("created_at", "updated_at")


class StudioStorageInline(admin.TabularInline):
    model = StudioStorage
    extra = 0
    fields = ('file', 'created_at', 'file_link')
    readonly_fields = ('created_at', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"

    file_link.short_description = 'File Link'


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(mode="text")}
    }

    model = Studio
    list_display = ("id", "user", "file_count", "created_at", "updated_at")
    search_fields = ("id", "user__username", "user__email")
    list_filter = ("created_at", "updated_at")
    inlines = [StudioStorageInline]

    def file_count(self, obj):
        return obj.studio_files.count()
    file_count.short_description = 'Number of Files'

    def change_view(self, request: HttpRequest, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

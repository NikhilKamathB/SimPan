from django.contrib import admin
from django.db.models import JSONField
from django.http import HttpRequest
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django_json_widget.widgets import JSONEditorWidget
from db.models import *


@admin.register(CeleryTask)
class CelryTaskAdmin(admin.ModelAdmin):

    model = CeleryTask
    list_display = ("task_id", "queue_name", "task_name", "task_type", "status", "created_at")
    search_fields = ("task_id", "queue_name", "task_name", "task_type")
    list_filter = ("queue_name", "task_name", "task_type", "status", "created_at")


@admin.register(WorkspaceStorage)
class WorkspaceStorageAdmin(admin.ModelAdmin):

    model = WorkspaceStorage
    list_display = ("id", "file", "created_at", "updated_at")
    search_fields = ("file",)
    list_filter = ("created_at", "updated_at")


class WorkspaceStorageInline(admin.TabularInline):
    model = WorkspaceStorage
    extra = 0
    fields = ('file', 'created_at', 'file_link')
    readonly_fields = ('created_at', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"

    file_link.short_description = 'File Link'

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(mode="text")}
    }

    model = Workspace
    list_display = ("id", "user", "file_count", "created_at", "updated_at")
    search_fields = ("id", "user__username", "user__email")
    list_filter = ("created_at", "updated_at")
    inlines = [WorkspaceStorageInline]

    def file_count(self, obj):
        return obj.workspace_files.count()
    file_count.short_description = 'Number of Files'

    def change_view(self, request: HttpRequest, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
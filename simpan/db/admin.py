from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from db.models import *

@admin.register(CeleryTask)
class CelryTaskAdmin(admin.ModelAdmin):

    model = CeleryTask
    list_display = ("task_id", "queue_name", "task_name", "task_type", "status", "created_at")
    search_fields = ("task_id", "queue_name", "task_name", "task_type")
    list_filter = ("queue_name", "task_name", "task_type", "status")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode="form")},
    }

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
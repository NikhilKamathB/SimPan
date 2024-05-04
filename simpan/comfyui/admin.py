from django.contrib import admin
from comfyui.models import CeleryTask


class CelryTaskAdmin(admin.ModelAdmin):

    model = CeleryTask
    list_display = ("task_id", "queue_name", "task_name", "task_type", "status", "created_at")
    search_fields = ("task_id", "queue_name", "task_name", "task_type")
    list_filter = ("queue_name", "task_name", "task_type", "status")


admin.site.register(CeleryTask, CelryTaskAdmin)

from django.db import models
from comfyui.constants import INITIATED, CELERY_TASK_STATUS


class CeleryTask(models.Model):

    class Meta:
        verbose_name = "Celery Task"
        verbose_name_plural = "Celery Tasks"

    task_id = models.CharField(max_length=255, unique=True)
    queue_name = models.CharField(max_length=255)
    task_name = models.CharField(max_length=255)
    task_type = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=CELERY_TASK_STATUS, default=INITIATED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.task_id

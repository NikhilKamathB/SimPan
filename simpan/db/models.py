import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from db.utils import get_workspace_file_path


class CeleryTaskStatus(models.TextChoices):

    INITIATED = "Initiated", _("Initiated")
    COMPLETED = "Completed", _("Completed")
    ABORTED = "Aborted", _("Aborted")


class CeleryTask(models.Model):

    class Meta:
        verbose_name = "Celery Task"
        verbose_name_plural = "Celery Tasks"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    task_id = models.CharField(max_length=255, unique=True)
    queue_name = models.CharField(max_length=255)
    task_name = models.CharField(max_length=255)
    task_type = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=CeleryTaskStatus.choices, default=CeleryTaskStatus.INITIATED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.task_id
    

class WorkspaceStorage(models.Model):

    class Meta:
        verbose_name = "Workspace Storage"
        verbose_name_plural = "Workspace Storages"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE, related_name="workspace_files")
    file = models.FileField(upload_to=get_workspace_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.file.name if self.file else str(self.id)


class Workspace(models.Model):

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, null=True, blank=True)
    conversation = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete_file_object(self, file_obj_id: models.UUIDField) -> None:
        self.workspace_files.delete(id=file_obj_id)

    def __str__(self) -> str:
        return str(self.id)
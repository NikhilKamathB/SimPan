import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from workspace.utils import get_studio_file_path


class StudioStorage(models.Model):

    class Meta:
        verbose_name = "Studio Storage"
        verbose_name_plural = "Studio Storages"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    studio = models.ForeignKey(
        "Studio", on_delete=models.CASCADE, related_name="studio_files")
    file = models.FileField(upload_to=get_studio_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.file.name if self.file else str(self.id)


class Studio(models.Model):

    class Meta:
        verbose_name = "Studio"
        verbose_name_plural = "Studios"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    conversation = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="studio_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete_file_object(self, file_obj_id: models.UUIDField) -> None:
        self.studio_files.delete(id=file_obj_id)

    def __str__(self) -> str:
        return str(self.id)
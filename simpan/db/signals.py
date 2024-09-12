from django.dispatch import receiver
from django.db.models.signals import pre_delete
from db.models import WorkspaceStorage


@receiver(pre_delete, sender=WorkspaceStorage)
def delete_workspace_storage_on_instance_delete(sender, instance, **kwargs):
    if instance.file: instance.file.delete()
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from workspace.models import StudioStorage


@receiver(pre_delete, sender=StudioStorage)
def delete_studio_storage_on_instance_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete()
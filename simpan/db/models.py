from django.db import models
from django.utils.translation import gettext_lazy as _


class JobSource(models.TextChoices):

    INDEED = "indeed", _("Indeed")
    LINKEDIN = "linkedin", _("LinkedIn")
    GLASSDOOR = "glassdoor", _("Glassdoor")


class CeleryTaskStatus(models.TextChoices):

    INITIATED = "Initiated", _("Initiated")
    COMPLETED = "Completed", _("Completed")
    ABORTED = "Aborted", _("Aborted")


class CeleryTask(models.Model):

    class Meta:
        verbose_name = "Celery Task"
        verbose_name_plural = "Celery Tasks"

    task_id = models.CharField(max_length=255, unique=True)
    queue_name = models.CharField(max_length=255)
    task_name = models.CharField(max_length=255)
    task_type = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=CeleryTaskStatus.choices, default=CeleryTaskStatus.INITIATED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.task_id


class Job(models.Model):

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
    
    job_source = models.CharField(max_length=15, choices=JobSource.choices, verbose_name=_("Job Source"))
    job_data = models.JSONField(verbose_name=_("Job Data"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.pk} - {self.job_source}"

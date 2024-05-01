from workers import *
from celery import Celery
from celery.worker.request import Request


app = Celery("sdc")
app.config_from_object(sdc_config)
app.autodiscover_tasks(["workers.tasks.sdc_task"])

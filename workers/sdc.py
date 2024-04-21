from workers import *
from celery import Celery


app = Celery(
    name="sdc",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
    include=["workers.tasks.sdc_task"],
)
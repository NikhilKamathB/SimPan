from kombu import Queue, Exchange
from workers.validators import ExchangeName, QueueName, RoutingKey
        
broker_url = "amqp://guest:guest@localhost:5672//"
result_backend = "rpc://"
sdc_exchange = Exchange(ExchangeName.SDC.value, type="direct")
task_queues = [
    Queue(
        QueueName.SDC.value, 
        routing_key=RoutingKey.SDC.value,
        exchange=sdc_exchange)
]
task_ack_late = True
worker_concurrency = 1
worker_prefetch_multiplier = 1
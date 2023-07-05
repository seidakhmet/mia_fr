import os

from celery import Celery
from kombu import Exchange, Queue

from .delayed_queues import get_delayed_task_delivery_kit


if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("mia_fr")

queues_for_delayed_task_delivery = get_delayed_task_delivery_kit()


app.conf.task_queues = [
    Queue("mia-fr", Exchange("mia-fr"), routing_key="mia-fr"),
    queues_for_delayed_task_delivery.destination_queue,
]

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

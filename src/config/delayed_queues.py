"""Модуль очередей для отложенных задач, предоставляет очереди и точку обмена для задач celery."""

from typing import NamedTuple

from kombu import Exchange, Queue


class DelayedTaskDeliveryKit(NamedTuple):
    destination_queue: Queue
    destination_exchange: Exchange
    routing_key: str


def get_delayed_task_delivery_kit(
    destination_queue_name: str = "auto-celery-delayed-tasks",
) -> DelayedTaskDeliveryKit:
    """
    https://stackoverflow.com/questions/35449234/how-could-i-send-a-delayed-message-in-rabbitmq-using-the-rabbitmq-delayed-messag
    """
    # Чтобы использовать функцию отложенного обмена сообщениями, нужно объявить обмен с типом x-delayed-message.
    destination_exchange = Exchange(
        destination_queue_name,
        type="x-delayed-message",
        arguments={"x-delayed-type": "direct"},
    )
    destination_queue = Queue(
        destination_queue_name,
        exchange=destination_exchange,
        routing_key=destination_queue_name,
    )
    return DelayedTaskDeliveryKit(
        destination_queue=destination_queue,
        destination_exchange=destination_exchange,
        routing_key=destination_queue_name,
    )

import json
from kafka import KafkaConsumer
import django

django.setup()
from reporting_service.models.order import Order, OrderEvent
from reporting_service.event_store import DjangoEventStore


def main():
    consumer = KafkaConsumer(
        'order.status.changed',
        group_id=None,
        auto_offset_reset='latest',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    event_store = DjangoEventStore(aggregate_model=Order, event_model=OrderEvent)
    for msg in consumer:
        print(msg)
        order_id = msg.value.pop('order_id')
        event_store.append_to_stream(order_id, [msg.value])
        print('Successfully appended to stream')


if __name__ == '__main__':
    main()

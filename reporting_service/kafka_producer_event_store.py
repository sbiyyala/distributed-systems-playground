#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from kafka import KafkaProducer
import datetime
import json
import time

EVENT_STATUSES = {'Payment Succeeded', 'Payment Rejected', 'Shipped', 'Need Attention'}
TOPIC = 'order.status.changed'
PRODUCER = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def on_success(record):
    print('Successfully sent:')
    print(record)


def create_orders(seed_id, span):
    for order_id in range(seed_id, span):
        publish_msg({
            'event_date': datetime.datetime.today().date().isoformat(),
            'order_id': order_id,
            'name': 'Created'
        })


def simulate_order_changes(seed_id, span):
    order_ids = set(range(seed_id, span))

    while True:
        status = random.choice(tuple(EVENT_STATUSES))
        order_id = random.choice(tuple(order_ids))
        publish_msg({
            'event_date': datetime.datetime.today().date().isoformat(),
            'order_id': order_id,
            'name': status
        })
        time.sleep(5)


def publish_msg(payload, topic=TOPIC, producer=PRODUCER):
    producer.send(
        topic=topic,
        key=bytes('dummy key', encoding='utf-8'),
        value=payload
    ).add_callback(on_success)


def produce(order_start_idx, number_of_orders, create=True):
    """Simulate create order events(if create=True), followed by simulating
    random order event states
    """
    if create:
        create_orders(order_start_idx, number_of_orders)
    simulate_order_changes(order_start_idx, number_of_orders)


if __name__ == '__main__':
    produce(order_start_idx=1, number_of_orders=10, create=False)

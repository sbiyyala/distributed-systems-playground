#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import random
from kafka import KafkaProducer
import datetime
import json

EVENT_STATUS = {'Created', 'Payment Succeeded', 'Payment Rejected', 'Canceled', 'Shipped'}

def on_success(record):
    print('success-dance.gif')
    print(record)

def main(argv):
    # give broker IP from docker, once dockerized
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    order_id = 0
    while True:
        producer.send(
            topic='order.created',
            key=bytes('dummy key', encoding='utf-8'),
            value={
                'event_date': datetime.datetime.today().date().isoformat(),
                'order_id': order_id,

            }
        ).add_callback(on_success)
        order_id += 1
        time.sleep(5)


if __name__ == '__main__':
    exit(main(sys.argv))

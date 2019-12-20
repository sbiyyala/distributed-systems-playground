#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import random
from kafka import KafkaProducer
import datetime
import json


def on_success(record):
    print('success-dance.gif')
    print(record)

def main(argv):
    # give broker IP from docker, once dockerized
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    while True:
        # generate a random integer
        num = random.randint(10, 100)
        producer.send(
            topic='order.created',
            key=bytes('dummy key', encoding='utf-8'),
            value={'date_created': datetime.datetime.today().date().isoformat(), 'order_value': num}
        ).add_callback(on_success)
        # wait 1 second
        time.sleep(5)


if __name__ == '__main__':
    exit(main(sys.argv))

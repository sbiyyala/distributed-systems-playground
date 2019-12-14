#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import random
from kafka import KafkaProducer


def main(argv):
    # give broker IP from docker, once dockerized
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        # generate a random integer
        num = random.randint(0, 10)

        # message value and key must be raw bytes
        num_bytes = bytes("msg - " + str(num), encoding='utf-8')

        # send to topic on broker
        producer.send(
            topic='es-test',
            key=num_bytes,
            value=num_bytes)

        # wait 1 second
        time.sleep(1)


if __name__ == '__main__':
    exit(main(sys.argv))

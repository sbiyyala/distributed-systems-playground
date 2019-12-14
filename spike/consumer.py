#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from kafka import KafkaConsumer


def consumer_ready(consumer):
    partitions = None
    while partitions is None or len(partitions) == 0:
        partitions = consumer.partitions_for_topic('es-test')
        consumer.poll(20)


def main(argv):
    while True:
        # initialize consumer to given topic and broker
        consumer = KafkaConsumer('es-test',
                                 group_id=None,
                                 auto_offset_reset='earliest',
                                 bootstrap_servers=['localhost:9092'])
        consumer_ready(consumer)
        # loop and print messages
        for msg in consumer:
            print(msg)


if __name__ == '__main__':
    exit(main(sys.argv))
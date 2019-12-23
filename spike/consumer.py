#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from kafka import KafkaConsumer


def consumer_ready(consumer):
    partitions = None
    while partitions is None or len(partitions) == 0:
        partitions = consumer.partitions_for_topic('event-source-test')
        consumer.poll(20)


def main(argv):
    consumer = KafkaConsumer('event-source-test',
                             group_id=None,
                             auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'])
    # consumer_ready(consumer)
    # loop and print messages
    for msg in consumer:
        print(msg)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

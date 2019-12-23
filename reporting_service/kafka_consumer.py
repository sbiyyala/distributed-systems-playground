import json
from kafka import KafkaConsumer
import django

django.setup()
from reporting_service.models.order import Order


def main():
    consumer = KafkaConsumer(
        'order.created',
        group_id=None,
        auto_offset_reset='latest',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for msg in consumer:
        print(msg)
        order = Order(order_value=msg.value['order_value'], order_date=msg.value['date_created'])
        order.save()
        print('New order {} successfully saved'.format(order.id))


if __name__ == '__main__':
    main()

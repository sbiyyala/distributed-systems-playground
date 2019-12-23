import unittest
from ..event_store import EventStore
import django

django.setup()
from ..models.order import OrderEvent, Order
from django.test import TestCase


class TestEventStore(TestCase):
    def setUp(self) -> None:
        self.store = EventStore(aggregate_model=Order, event_model=OrderEvent)
        self.order_id = 200
        self.store.append_to_stream(
            self.order_id,
            [
                {'event_date': '2019-01-01', 'name': 'Begin'},
                {'event_date': '2019-01-02', 'name': 'Halt'},
                {'event_date': '2019-01-03', 'name': 'Think'},
                {'event_date': '2019-01-04', 'name': 'Proceed'},
            ]
        )

    def test_append_to_stream(self):
        # function under test is inside setup
        self.assertEqual(OrderEvent.objects.filter(aggregate__pk=self.order_id).count(), 4)
        order = Order.objects.get(pk=self.order_id)
        self.assertEqual(order.status, 'Proceed')

    def test_load_stream(self):
        event_stream = self.store.load_stream(self.order_id)
        self.assertEqual(
            ['Begin', 'Halt', 'Think', 'Proceed'],
            [event.name for event in event_stream]
        )


if __name__ == '__main__':
    unittest.main()

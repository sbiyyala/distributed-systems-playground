from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Order, OrderEvent
import json
from .event_store import DjangoEventStore


def detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = {
        'id': order.id,
        'status': order.status
    }
    return HttpResponse(content=json.dumps(data))


def history(request, order_id):
    get_object_or_404(Order, id=order_id)
    store = DjangoEventStore(aggregate_model=Order, event_model=OrderEvent)
    stream = store.load_stream(order_id)
    return HttpResponse(
        content=[
            {
                'event_status': event.name,
                'event_date': event.event_date
            }
            for event in stream
        ]
    )

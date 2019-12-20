from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Order
import json


def detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = {
        'id': order.id,
        'charged_amt': order.order_value,
        'date_created': order.order_date.isoformat()
    }
    return HttpResponse(content=json.dumps(data))

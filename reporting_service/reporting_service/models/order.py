from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_value = models.FloatField(default=0.0)
    status = models.CharField(max_length=100, default='new')

    objects = models.Manager()

    class Meta:
        app_label = 'reporting_service'


class OrderEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    aggregate = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='events', default=None, db_index=True)
    name = models.CharField(max_length=100)
    event_date = models.DateField()

    objects = models.Manager()

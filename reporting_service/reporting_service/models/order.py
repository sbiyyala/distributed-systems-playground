from django.db import models
import uuid


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    order_value = models.FloatField(default=0.0)
    objects = models.Manager()

    class Meta:
        app_label = 'reporting_service'

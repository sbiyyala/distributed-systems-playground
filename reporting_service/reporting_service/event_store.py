from typing import List, Dict
import uuid

PK = 'pk'
ID = 'id'


class DjangoEventStore(object):
    """A simple event store implemented for django models"""
    def __init__(self, aggregate_model, event_model):
        self.aggregate_model = aggregate_model
        self.event_model = event_model

    def load_stream(self, aggregate_id) -> List:
        """Given an aggregate id, fetch all events that roll up to the aggregate instance"""
        return self.event_model.objects.filter(**{'aggregate__pk': aggregate_id})

    def append_to_stream(self, aggregate_id,
                         event_stream: List[Dict]):  # todo: take care of concurrency here. Optimistic?
        aggregate, _ = self.aggregate_model.objects.get_or_create(pk=aggregate_id)
        for event_dict in event_stream:
            event = self.event_model(**{
                **event_dict,
                **{'id': uuid.uuid4()},
                **{'aggregate': aggregate}
            })
            event.save()
            self._save_aggregate(aggregate, **event_dict)
            print(
                f'Event {self.event_model.__name__} successfully appended to stream of {self.aggregate_model.__name__}'
                f' with id {aggregate_id}'
            )

    def _save_aggregate(self, aggregate, **event_dict):
        """
        Bespoke implementation of updating and saving aggregate instance. Currently expecting aggregate model
        to have a field called `Status` and incoming event to have a key called `name`.
        TODO: Use Adapter pattern to dynamically update aggregate model
        """
        try:
            setattr(aggregate, 'status', event_dict['name'])
            aggregate.save()
        except KeyError:
            pass

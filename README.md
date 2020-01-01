# distributed-systems-playground
## Overview
This creates a "hello world" microservices architecture on a simple scale using event sourcing

![Architecture](event_sourcing_playgound_arch.jpeg)

## Kafka
`$ cd kafka && docker-compose up` to stand up kafka/brokers

For a non-dockerized setup, refer to [spike/README](./spike/README.md)

### Running python producers/consumers
```bash
# Producer terminal
$ ./producer.py
# Consumer terminal
$ ./consumer.py
```  

### Reporting Service
This service has 2 "entry points":
* A consumer that listenens on `orders.status.changed` kafka topic and writes data into 
django models `Order` and `OrderEvent`
* A RESTful interface exposing:
    * /orders/<id>
    * /orders/<id>/history

#### Event Store
Reporting Service uses an event store class called `DjangoEventStore`. The idea is to expose
2 methods useful in event sourcing paradigm:
* `load_stream(aggreagate_id: Union[int, UUID)]) -> List[EventModle]`: Given an id of the
aggregate model, this will return a stream(a list for simplicity) of EventModel
* `append_to_stream(aggregate_id: Union[int, UUID], stream: List[Any])`: Appends a stream of 
events, rolled up under an aggregate model's instance 

#### Running Reporting Service
* To simulate a producer publishing order creation and order status change events, run
`reporting_service/kafka_producer_event_store.py`
* To consume the above msgs and write into reporting service's local event-store, run
`reporting_service/kafka_consumer.py`
* To query reporting service's REST interface, run django server
`./manage.py runserver` and hit any of the above listed endpoints

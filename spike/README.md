## Spike to have ensure kafka/zk is up/running

### Mac installation  
1. `$ brew install kafka`
2. `$ brew install zookeeper`

### Standup kafka & zk 
`$ zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties`

Append:
```
port = 9092
advertised.host.name = localhost

listeners=PLAINTEXT://:9092
```
to `/usr/local/etc/kafka/server.properties`

`$ kafka-server-start /usr/local/etc/kafka/server.properties`
 
#### Running producers and consumers from shell
```bash
# Create a kafka topic
$ kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <topic-name>
# Producer terminal
$ kafka-console-producer --broker-list localhost:9092 --topic <topic-name>
# Consumer terminal
$ kafka-console-consumer --bootstrap-server localhost:9092 --topic <topic-name> --from-beginning
```

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

##### Event Store
Reporting Service uses an event store class called `DjangoEventStore`. The idea is to expose
2 methods useful in event sourcing paradigm:
* `load_stream(aggreagate_id: Union[int, UUID)]) -> List[EventModle]`: Given an id of the
aggregate model, this will return a stream(a list for simplicity) of EventModel
* `append_to_stream(aggregate_id: Union[int, UUID], stream: List[Any])`: Appends a stream of 
events, rolled up under an aggregate model's instance 
    
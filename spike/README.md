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
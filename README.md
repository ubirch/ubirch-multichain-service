# ubirch-multichain-service
This is a command line interface python service developed to anchor data on a MultiChain 2.0 Blockchain.<br>
Multichain is a permissioned blockchain which means that is you want an address to be able to publish on a stream for
instance, you have to grant it enough rights to do so (1... here means a multichain address):

    grant 1... send
    grant 1... stream1.write
   

## Configuration

This projects uses python 3.6. <br>
Please run in your virtual environment:
   ```bash
        pip install -r requirements.txt
   ```

## How to use this service

1. Please install [Elasticmq](https://github.com/adamw/elasticmq) and/or [Kafka](https://kafka.apache.org/).
Please respect the following folder structure: <br>

        dependencies/
        ├── elasticMQServer
        │   ├── custom.conf
        │   └── elasticmq-server.jar
        └── kafka
            ├── bin
            │   ├── ...
            ├── config
            │   ├── ...
            ├── libs
            │   ├──...
            ├── LICENSE
            ├── NOTICE
            └── site-docs
                └── ...

And custom.conf should look like this:

        include classpath("application.conf")
        
        // What is the outside visible address of this ElasticMQ node
        // Used to create the queue URL (may be different from bind address!)
        node-address {
            protocol = http
            host = localhost
            port = 9324
            context-path = ""
        }
        
        rest-sqs {
            enabled = true
            bind-port = 9324
            bind-hostname = "0.0.0.0"
            // Possible values: relaxed, strict
            sqs-limits = strict
        }
        
        // Should the node-address be generated from the bind port/hostname
        // Set this to true e.g. when assigning port automatically by using port 0.
        generate-node-address = false
        
        queues {
        
          input {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "queue1-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }
        
            output {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "queue2-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }
        
            errors {
            defaultVisibilityTimeout = 10 seconds
            receiveMessageWait = 0 seconds
            deadLettersQueue {
                name = "error_queue-dead-letters"
                maxReceiveCount = 10 // from 1 to 1000
            }
          }
        
        }
        


2. Useful scripts are in *bin/* <br>
    a) In *bin/elasticMQ/*, to run the ElasticMQ server: <br>
      ```bash
      ./start-elasticMQ.sh
      ```
       
    b) In *bin/kafka/*, to run the Kafka server and create the topics, execute successively: <br>
     ```bash

        ./start_zookeeper.sh
        ./start-kafka.sh
        ./create-all-topics.sh
     
    ```
        
3. Then, in a terminal, run successively in *ubirch-multichain-service/*, the scripts *sender.py* then *receiver.py*
and *receiver_errors.py*, with the flag **--server='SQS'** or **--server='KAFKA'**<br><br>

2. [Install MultiChain 2.0](https://www.multichain.com/download-install/)
 
3. Set up a MultiChain blockchain or connect to an existing one.
<br>You can check out the MultiChain [getting started page](https://www.multichain.com/getting-started/) for more details.

4. Finally, start the service.<br>

    ```bash
    python multichain_service.py --server=$SERVER --key=$KEY --stream=$STREAM_NAME
    ```
Other parameters are set by default by are configurable. <br>
   
Help concerning the CLI can be found running:
```bash
python multichain_service.py --help
```
Messages are sent into a multichain stream with a configurable key.<br>
To query the stream's content, run in the multichain-cli:

    subscribe STREAM_NAME
    
    liststreamitems STREAM_NAME # To retrieve all stream items
    
    liststreamkeys STREAM_NAME  # To retrieve all stream keys
    
    liststreamqueryitems STREAM_NAME '{"keys":["key1", "key2"]}' # To retrieve items by keys or list of keys
    
    getstreamitem STREAM_NAME txid  # To retrieve an item on the stream by its txid
    
    liststreampublishers STREAM_NAME    # To retrieve all the publishers of the stream
    
    liststreampublisheritems STREAM_NAME 1...   # To retrieve all published items by a given address


If you want additional information concerning the way streams can be used, please consult the 
[full list of JSON-RPC-API commands](https://www.multichain.com/developers/json-rpc-api/)
    
## Docker


## Logs


Once the service is running, logs are recorded in *multichain_service.log* as well as displayed in the terminal.

# License 

This project is publicized under the [Apache License 2.0](LICENSE).


# ubirch-multichain-service
A MultiChain based anchoring service.
This service uses Apache Kafka for messaging.

# Configuration
This projects uses Python 3. <br>
Please, run in your virtual environment:

        pip3 install -r requirements.txt

1. Set up the [Kafka]((https://kafka.apache.org/)) server. Useful bash scripts are in bin/ ( ./start-zookeeper.sh, ./start-kafka.sh and./create-all-topics.sh).<br> Three topics should be created : queue1, queue2 and errorQueue. <br>


2. [Install MultiChain](https://www.multichain.com/download-install/)
 
 
3. Set up a MultiChain blockchain. You can check out [this link](https://www.multichain.com/developers/creating-connecting/) or the MultiChain [getting started page](https://www.multichain.com/getting-started/) for more details.


        multichain-util create [chain-name]
       
And to connect to connect to an existing chain : 
        
        
        multichaind [chain-name] -daemon

4. Start the sender process which will send random hashes & error messages in the topic queue1.

5. Start the MultiChain service :

-Sends error (non hex messages and timeouts) in the errorQueue.<br>
-Sends JSON docs containing the txid and the input data in queue2 if the anchoring was successful.

6.. Start the receivers services (receiver.py and receiver_errors.py) which will listen to the topics queue2 and errorQueue.

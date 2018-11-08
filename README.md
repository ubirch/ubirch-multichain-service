# ubirch-iota-service
A MultiChain based anchoring service.

# Configuration
This projects uses Python 3. <br>
Please, run in your virtual environment:

        pip3 install -r requirements.txt
       
[MultiChain](https://www.multichain.com/download-install/) and [Kafka](https://kafka.apache.org/) need to be properly installed. <br>

Third party libraries in Python: [Savoir by DXMarkets](https://github.com/DXMarkets/Savoir), which implements the MultiChain core API.<br>

## How to use this service :

1. Set up the Kafka server. Useful bash scripts are in bin/. Three topics should be created : queue1, queue2 and errorQueue. <br>

2. Set up a multichain blockchain. You can check out [this link](https://www.multichain.com/developers/creating-connecting/) or the MultiChain [getting started page](https://www.multichain.com/getting-started/) for more details.


        multichain-util create [chain-name]
       
And to connect to connect to an existing chain : 
        
        
        multichaind chain1 -daemon

3. Start the sender process which will send random hashes & error messages in the topic queue1.

4. Start the multichain service :

-Sends error (non hex messages and timeouts) in the errorQueue.<br>
-Sends JSON docs containing the txid and the input data in queue2 if the anchoring was successful.

5. Start the receivers services (receiver.py and receiver_errors.py) which will listen to the topics queue2 and errorQueue.

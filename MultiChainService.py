# coding: utf-8
#
# ubirch anchoring
#
# @author Victor Patrin
#
# Copyright (c) 2018 ubirch GmbH.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from library import *
from Savoir import *
import json
import subprocess

args = set_arguments("MultiChain")
port = args.port

#Kafka
producer = producerInstance(port)
queue1 = consumerInstance('queue1', port)
queue2 = consumerInstance('queue2', port)
errorQueue = consumerInstance('errorQueue', port)

#  3rd party lib not working well
#
# rpcuser = args.rpcuser
# rpcpasswd = args.rpcpasswd
# rpchost = args.rpchost
# rpcport = args.rpcport
# chainname = args.chainname
# api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
# print(api.getinfo().decode('utf-8'))



#TODO : PASS THESE AS ARGS

path = "/usr/local/bin/multichain-cli"
chain = "ubirch-multichain"

def APIcall(chain,command):
    output = subprocess.check_output([path, chain, command]).decode("utf-8")
    print(output)
    return(json.loads(output))

# getinfo = 'getinfo'
# APIcall(chain, command)

#TODO : WALLET MANAGEMENT
#TODO : ubirch-python-utils integration after kafka debugging

def genaddress():
    return APIcall(chain, "getnewaddress")

def listaddresses():
    return APIcall(chain, "getaddresses")

listaddresses()


#TODO : STORESTRING FUNC

def storeStringMC(string):
    if is_hex(string):



        #txhash =
        print({'status': 'added', 'txid': txhash, 'message': string})

        return {'status': 'added', 'txid': txhash, 'message': string}

    else:
        return False

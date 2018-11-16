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
import json
import subprocess

args = set_arguments("MultiChain")
port = args.port

#Kafka
producer = producerInstance(port)
queue1 = consumerInstance('queue1', port)
queue2 = consumerInstance('queue2', port)
errorQueue = consumerInstance('errorQueue', port)

# from Savoir import *
# 3rd party lib not working well
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


def apicall(chain, command):
    command_split = command.split(" ")
    print(command_split)
    output = subprocess.check_output([path, chain] + command_split).decode("utf-8")
    print("Ouput of command '%s' is : \n %s \n" %(command, output))
    return output

# getinfo = 'getinfo'
# apicall(chain, getinfo)

#TODO : ubirch-python-utils integration after kafka debugging

#TODO : make command parser for APIcall !!!!!

#TODO : WALLET AND PERMISSION MANAGEMENT

def genaddress():
    return apicall(chain, "getnewaddress")

admin_address = "1Gynv7tHvXW2j643Ah6rmP2MnsPvVAQkYA6C9q"

def listaddresses():
    return apicall(chain, "listaddresses")

def grantpermission(address, permission):
    command = "grant %s %s" %(address, permission)
    return apicall(chain, command)


## ASSET ISSUANCE


def createnewasset(issuing_address, asset_name, asset_qty): #'open':true means asset can be issued after being created
    command = "issuefrom %s %s '{'name':%s,'open':true}' %d" %(issuing_address, issuing_address, asset_name, asset_qty)
    return apicall(chain, command)

## Working great !Gynv7tHvXW2j643Ah6rmP2MnsPvVAQkYA6C9q
# createnewasset(admin_address, "test", 10000)


def issuemore(issuing_address, recipient, asset_name, asset_qty):
    command = "issuemorefrom %s %s %s %d" %(issuing_address, recipient, asset_name, asset_qty)
    return apicall(chain, command)

apicall(chain, 'listassets')
## Working great!
#createnewasset(admin_address, 'eur', 5000)
issuemore(admin_address, admin_address, 'eur', 5000)


# TODO : STORESTRING FUNC


# def storestringmc(string):
#     if is_hex(string): #Make Transaction
#
#         print({'status': 'added', 'txid': txhash, 'message': string})
#         return {'status': 'added', 'txid': txhash, 'message': string}
#
#     else: #Return error
#         return False

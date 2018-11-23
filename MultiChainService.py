# coding: utf-8
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


from ubirch.anchoring_kafka import *
from kafka import *
import subprocess

args = set_arguments("MultiChain")
port = args.port

#Kafka
producer = KafkaProducer(bootstrap_servers=port)
queue1 = KafkaConsumer('queue1', bootstrap_servers=port)


#TODO : PASS THESE AS ARGS

path = "/usr/local/bin/multichain-cli"
chain = "ubirch-multichain"

#TODO : make command parser for APIcall !!!!!

def apicall(chain, command):
    command_split = command.split(" ")
    print(command_split)
    output = subprocess.check_output([path, chain] + command_split).decode("utf-8")
    print("Ouput of command '%s' is : \n %s \n" %(command, output))
    return output


# WALLET AND PERMISSION MANAGEMENT


def genaddress():
    return apicall(chain, "getnewaddress")


def listaddresses():
    return apicall(chain, "listaddresses")


def grantpermission(address, permission):
    command = "grant %s %s" %(address, permission)
    return apicall(chain, command)


def sendasset(asset, receiver, qty):
    command = "sendasset %s %s %d" %(receiver, asset, qty)
    return apicall(chain, command)


#               ASSET ISSUANCE


def createnewasset(issuing_address, asset_name, asset_qty): #'open':true means asset can be issued after being created
    command = "issue %s {'name':%s,'open':true} %d" %(issuing_address, asset_name, asset_qty)
    return apicall(chain, command)


def issuemore(recipient, asset_name, asset_qty):
    command = "issuemore %s %s %d" %(recipient, asset_name, asset_qty)
    return apicall(chain, command)


admin_address = '1Gynv7tHvXW2j643Ah6rmP2MnsPvVAQkYA6C9q'
receiver_address = '1KSawFvmrWypch3CMG14LcH1GX8UK9wAMPzgVT'

#createnewasset(admin_address, 'eur3', 5000)
#apicall(chain, 'listassets')
#issuemore(admin_address, "'{'name':'eur','open':true}'", 5000)
#listaddresses()

# grantpermission(admin_address, 'send')
# grantpermission(receiver_address, 'receive')
# sendasset("dollars", receiver_address, 1)

# TODO : STORESTRING FUNC


def storestringmc(message):
    if is_hex(message):
        txhash = sendasset("dollars", receiver_address, 1).split('\n')[0]

        print({'status': 'added', 'txid': txhash, 'message': message})
        return {'status': 'added', 'txid': txhash, 'message': message}

    else:
        return False


def main(storefunction):
    """Continuously polls the topic for messages"""
    while True:
        poll(queue1, 'errorQueue', 'queue2', storefunction, producer)


main(storestringmc)
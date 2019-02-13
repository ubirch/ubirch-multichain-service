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


import subprocess
from ubirch.anchoring import *
from kafka import *


import logging
from logging.handlers import RotatingFileHandler


"""
    The code below is used to initialize parameters passed in arguments in the terminal.
    Before starting the service one must choose between --server='SQS' or --server='KAFKA' depending on the message
    queuing service desired.
    Depending on the server chosen, several arguments of configuration of the latest are initialized.

"""
args = set_arguments("multichain")
server = args.server

"""
    Logger & handlers configuration
"""

log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
}


logger = logging.getLogger('ubirch-iota-service')
level = log_levels.get(args.loglevel.lower())
logger.setLevel(level)


# Formatter adding time, name and level of each message when a message is written in the logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Handler redirecting logs in a file in 'append' mode, with 1 backup and 1Mo max size
file_handler = RotatingFileHandler('iota_service.log', mode='a', maxBytes=1000000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler on the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


logger.info("You are using ubirch's IOTA anchoring service")

if server == 'SQS':
    logger.info("SERVICE USING SQS QUEUE MESSAGING")

    url = args.url
    region = args.region
    aws_secret_access_key = args.accesskey
    aws_access_key_id = args.keyid

    input_messages = get_queue(args.input, url, region, aws_secret_access_key, aws_access_key_id)
    output_messages = get_queue(args.output, url, region, aws_secret_access_key, aws_access_key_id)
    error_messages = get_queue(args.errors, url, region, aws_secret_access_key, aws_access_key_id)
    producer = None

elif server == 'KAFKA':
    logger.info("SERVICE USING APACHE KAFKA FOR MESSAGING")

    output_messages = args.output
    error_messages = args.errors

    bootstrap_server = args.bootstrap_server
    producer = KafkaProducer(bootstrap_servers=bootstrap_server)
    input_messages = KafkaConsumer(args.input, bootstrap_servers=bootstrap_server)

'''
    Multichain configuration:
        -chain name
        -path to multichain-cli
        -name of the stream used to publish data
        -key used to publish data on the stream
'''
path_cli = args.path
chain_name = args.chain
stream_name = args.stream
key = args.key


def api_call(command):
    """

    :param command: command destined to be sent to the multichain-cli
    :return: the output of the command
    """
    command_split = command.split(" ")
    logger.debug(command_split)

    output = subprocess.check_output([path_cli, chain_name] + command_split).decode("utf-8")
    logger.debug("Ouput of command '%s' is : \n %s \n" % (command, output))

    return output


def store_multichain(string):
    """

    :param string: message to be sent in the IOTA transaction
    :return: If the input string is hexadecimal : a dictionary containing the string sent in the transaction
    and the transaction hash.
            If not : False
    :rtype: Dictionary if the input string is hexadecimal or boolean if not.

    """
    if is_hex(string):
        logger.debug("'%s' ready to be sent" % string)
        
        command = "publish %s %s %s" % (stream_name, key, string)
        tx_hash = api_call(command).split('\n')[0]

        logger.debug("'%s' sent" % string)
        logger.info({'status': 'added', 'txid': tx_hash, 'message': string})
        return {'status': 'added', 'txid': tx_hash, 'message': string}

    else:
        logger.warning({"Not a hash": string})
        return False


def main(store_function):
    """

    Continuously polls the queue1 for messages and processes them in queue2 (sends the dict returned by storestringIOTA)
    or error_queue

    :param store_function: Defines the service used to anchor the messages. Here it is IOTA.

    """
    while True:
        poll(input_messages, error_messages, output_messages, store_function, server, producer)


main(store_multichain)

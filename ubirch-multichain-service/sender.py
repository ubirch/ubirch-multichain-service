# coding: utf-8

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

import time
import hashlib
from ubirch.anchoring import *
from kafka import *

args = set_arguments("multichain")
server = args.server

if server == 'SQS':
    print("SERVICE USING SQS QUEUE MESSAGING")
    print("input queue : %s" % args.input)

    url = args.url
    region = args.region
    aws_secret_access_key = args.accesskey
    aws_access_key_id = args.keyid

    input_messages = get_queue(args.input, url, region, aws_secret_access_key, aws_access_key_id)
    producer = None

elif server == 'KAFKA':
    print("SERVICE USING APACHE KAFKA FOR MESSAGING")
    print("input topic : %s" % args.input)

    input_messages = args.input
    bootstrap_server = args.bootstrap_server
    producer = KafkaProducer(bootstrap_servers=bootstrap_server)

i = 1
j = 1
while True:
    t = str(time.time()).encode('utf-8')
    message = hashlib.sha256(t).hexdigest()
    if '0' in message[0:8]:  # Error propagation in input_messages
        send("error %s" % i, server, queue=input_messages, topic=input_messages, producer=producer)
        print("error %s sent" % i)
        i += 1
        time.sleep(0.5)

    else:  # Sends in input_messages the sha256 hash of the time()
        send(message,  server, queue=input_messages, topic=input_messages, producer=producer)
        print("message %s sent" % message)
        j += 1
        time.sleep(0.5)


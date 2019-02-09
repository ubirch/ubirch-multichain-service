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

from ubirch.anchoring import *
from kafka import *

args = set_arguments("multichain")
server = args.server

if server == 'SQS':
    print("SERVICE USING SQS QUEUE MESSAGING")
    print("error queue name : %s" % args.errors)

    url = args.url
    region = args.region
    aws_secret_access_key = args.accesskey
    aws_access_key_id = args.keyid

    error_messages = get_queue(args.errors, url, region, aws_secret_access_key, aws_access_key_id)

    while True:
        errors = error_messages.receive_messages()
        for e in errors:
            print(e.body)
            e.delete()


elif server == 'KAFKA':
    print("SERVICE USING APACHE KAFKA FOR MESSAGING")
    print("error topic name : %s" % args.errors)

    bootstrap_server = args.bootstrap_server
    error_messages = KafkaConsumer(args.errors, bootstrap_servers=bootstrap_server,
                                   value_deserializer=lambda m: json.dumps(m.decode('ascii')))
    for message in error_messages:
        print(json.loads(message.value))

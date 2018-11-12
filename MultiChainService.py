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

args = set_arguments("MultiChain")
port = args.port
rpcuser = args.rpcuser
rpcpasswd = args.rpcpasswd
rpchost = args.rpchost
rpcport = args.rpcport
chainname = args.chainname

api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

api('getinfo')
#Kafka
producer = producerInstance(port)
queue1 = consumerInstance('queue1', port)
queue2 = consumerInstance('queue2', port)
errorQueue = consumerInstance('errorQueue', port)

#!/usr/bin/env bash

cd ../../dependencies/kafka_2.11-2.0.0
./bin/zookeeper-server-start.sh config/zookeeper.properties

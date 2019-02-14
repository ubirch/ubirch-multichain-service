#!/usr/bin/env bash

python multichain_service.py -s ${SERVER} -ll ${LOGLEVEL} -stream ${STREAM} -key ${KEY} -path ${PATH_CLI} -chain ${CHAIN_NAME} -bs ${KAFKA_BOOTSTRAP_SERVER} -i ${INPUT} -o ${OUTPUT} -e ${ERRORS}

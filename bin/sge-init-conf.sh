#!/bin/bash
WORK_ROOT=/usr/share/charm-sge-cluster
CONF_HOSTLIST=${WORK_ROOT}/hostlist.conf
CONF_SCHEDULER=${WORK_ROOT}/scheduler.conf
CONF_QUEUE=${WORK_ROOT}/queue.conf

qconf -as `hostname`

mkdir -p ${WORK_ROOT}

# create host list
qconf -Msconf ${CONF_SCHEDULER}

# create a host list
qconf -Ahgrp ${CONF_HOSTLIST}
# create the queue
qconf -Aq ${CONF_QUEUE}


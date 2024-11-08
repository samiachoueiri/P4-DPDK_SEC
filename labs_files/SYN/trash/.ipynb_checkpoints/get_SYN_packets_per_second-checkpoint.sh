#!/bin/bash

function count_syn_packets() {
    tcpdump -i enp7s0np0 'tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) = 0' -c $1 -w /dev/null 2>&1 | grep -o -E '[0-9]+ packets r' | awk '{print $1}' 
}

DURATION=1

echo "Waiting for SYN packets to be received ..."

while true; do

    SYN_COUNT=$(count_syn_packets $DURATION)

    echo "Received $SYN_COUNT SYN packets in the last second"

    sleep 1

done
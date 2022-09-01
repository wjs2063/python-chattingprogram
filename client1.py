#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 17:47:46 2022

@author: pn_jh
"""

from kafka import KafkaConsumer
from kafka import KafkaProducer
import sys
import os
from threading import Thread
from multiprocessing import Process
import json
# topic 의 1번파티션에서 읽고 0번파티션으로 전송

producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],api_version = (0,10,2),
                         key_serializer = str.encode,
                         compression_type='gzip'
                         )
consumer = KafkaConsumer('first_kafka01',bootstrap_servers = ['localhost:9092'],api_version = (0,10))


def send_message():
    text = ""
    while text != "exit":
        text = input()
        producer.send(topic = 'first_kafka01',value =json.dumps(text).encode(),key = '0')



def receive_message():
    for messages in consumer:
        message = messages.value.decode('utf-8')
        if message == 'exit':
            return print("채팅을 종료합니다")
        print(message)

print("함수시작")

send_thread    = Thread(target = send_message)
receive_thread = Thread(target = receive_message)


print('send_ thread 시작')
receive_thread.start()
send_thread.start()
print("receive_thread 시작")



send_thread.join()
receive_thread.join()
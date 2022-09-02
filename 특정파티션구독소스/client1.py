#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 17:47:46 2022

@author: pn_jh
"""

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import sys
import os
from threading import Thread
from multiprocessing import Process
import json
# topic 의 1번파티션에서 읽고 0번파티션으로 전송
TOPIC = 'chat-kafka01'


producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],api_version = (0,10,2),
                         #key_serializer = str.encode,
                         value_serializer = lambda v: json.dumps(v).encode('utf-8'),
                         compression_type='gzip'
                         )


consumer = KafkaConsumer(
                         bootstrap_servers = ['localhost:9092'],
                         api_version = (0,10),
                         
                         )
#해당 consumer 가 읽을 파티션 지정
consumer.assign([TopicPartition(TOPIC, 1)])

def send_message():
    text = ""
    while text != "exit":
        text = input()
        producer.send(topic = TOPIC,
                      value = text,
                      partition = 0)


def receive_message():
    #print(consumer.partitions_for_topic(topic = TOPIC))
    #print(TopicPartition(TOPIC, 0))
    print("-------시작합니다------")
    for messages in consumer:
        message = messages.value.decode('utf-8')
        if message == 'exit':
            return print("채팅을 종료합니다")
        print(message)
        print(f"수신받은 메세지 :{message} , 이 메세지는 partition : {messages.partition}, message_key : {messages.key} ,message offset: {messages.offset }")
print("채팅시작")

send_thread    = Thread(target = send_message)
receive_thread = Thread(target = receive_message)


print('send_ thread 시작')
receive_thread.start()
send_thread.start()
print("receive_thread 시작")



send_thread.join()
receive_thread.join()

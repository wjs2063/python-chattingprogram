#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 16:03:14 2022

@author: pn_jh
"""

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import sys
import os
from threading import Thread
from multiprocessing import Process
import json
# 토픽의 0번파티션에서 읽고 1번파티션으로 전송
# partition 으로 
TOPIC = 'chat-kafka01'
producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],
                         api_version = (0,10,2),
                        #key_serializer = str.encode,
                        value_serializer = lambda v: json.dumps(v).encode('utf-8'),
                        compression_type='gzip'
                        )

consumer = KafkaConsumer(
                         bootstrap_servers = ['localhost:9092'],
                         api_version = (0,10),
                         
                         )

#해당 consumer 가 읽을 파티션 지정
consumer.assign([TopicPartition(TOPIC, 0)])
def send_message():
    print("send_message 함수실행합니다")
    text = ""
    while text != "exit":
        text = input()
        producer.send(topic = TOPIC,
                      value = text,
                      partition = 1)


def receive_message():
    print("receive_message 함수실행")
    for messages in consumer:
        print("hello")
        message = messages.value.decode('utf-8')
        if message == 'exit':
            return print("채팅을 종료합니다")
        print(f"수신받은 메세지 :{message} , 이 메세지는 partition : {messages.partition}, message_key : {messages.key} ,message offset: {messages.offset }",)

print("채팅시작")

send_thread    = Thread(target = send_message )
receive_thread = Thread(target = receive_message )

# 스레드 시작 
print('send_ thread 시작')
receive_thread.start()
send_thread.start()
print("receive_thread 시작")




send_thread.join()
receive_thread.join()

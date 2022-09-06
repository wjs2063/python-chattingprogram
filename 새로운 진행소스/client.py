#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 18:03:04 2022

@author: pn_jh
"""
from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import sys
import os
from threading import Thread
from multiprocessing import Process
import json
import socket
import select
import sys

TOPIC = 'chat-kafka01'
# 소켓 연결
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))



def get_name_from_server():
    global s
    while True:
        read, write, fail = select.select((s, sys.stdin), (), ())
    
        for desc in read:
            if desc == s:
                data = s.recv(4096)
                msg = data.decode().split()
                name,partition, partner_partition = msg[0],int(msg[1]),int(msg[2])
                return name,partition,partner_partition
            
# producer 메세지를 보낼때 사용하는 message
def send_message(partner_partition):
    print("send_message 함수실행합니다")
    text = ""
    while text != "exit":
        text = input()
        producer.send(topic = TOPIC,
                      value = text,
                      partition = partner_partition)


def receive_message():
    print("receive_message 함수실행")
    for messages in consumer:
        print("hello")
        message = messages.value.decode('utf-8')
        if message == 'exit':
            return print("채팅을 종료합니다")
        print(f"수신받은 메세지 :{message} , 이 메세지는 partition : {messages.partition}, message_key : {messages.key} ,message offset: {messages.offset }",)




# 이름 받아오기
# 상대 에게 전송할 TOPIC과 partition 번호도 필요함
name,partition,partner_partition = get_name_from_server()
print(name,partition,partner_partition)
# 카프카 컨슈머,프로듀서 생성하기
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

# 컨슈머가 읽을 토픽과 파티션 지정 
consumer.assign([TopicPartition(TOPIC, partition)])

# send thread 와 receive thread 를 생성


send_thread    = Thread(target = send_message, args = (partner_partition,))
receive_thread = Thread(target = receive_message )

# 스레드 시작 
print('send_ thread 시작')
receive_thread.start()
send_thread.start()
print("receive_thread 시작")




send_thread.join()
receive_thread.join()
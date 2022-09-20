#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 17:52:03 2022

@author: pn_jh
"""
import os
from twisted.internet import protocol, reactor
import random
from collections import deque,defaultdict
import re
#서버 디렉토리 경로 변경


transports = set()
topics = set()
waited_queue = deque([])
users = set()
table = defaultdict(int)
class Chat(protocol.Protocol):
    def __init__(self):
        super().__init__()
        self._count = 1
        
    def delete_topic(self,name):
        cmd = f"/Users/pn_jh/Desktop/개발/kafka/kafka_2.13-3.2.0/bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic {name}"
        os.system(cmd)
        topics.discard(name)
    

    
    def produce_topic(self,name1,name2):
        name = str(name1) + str(name2)
        name = re.sub(r"[^a-zA-Z0-9]","",name)
        print(f"TOPIC 생성중 {name}")
        cmd = f'/Users/pn_jh/Desktop/개발/kafka/kafka_2.13-3.2.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1 --topic {name}'
        os.system(cmd)
        print("TOPIC 생성완료")
        topics.add(name)
        return name
    
    
    def matching(self):
        if len(waited_queue) < 2:
            print("잠시만 기다려주세요...")
            return -1
        # waited_queue 에서 A 정보
        A_transport = waited_queue.popleft()
        # waited_queue 에서 B 정보
        B_transport = waited_queue.popleft()
        # A 와 B 를 연결해줄 토픽 생성
        topic_name = self.produce_topic(A_transport,B_transport)
        
        table[A_transport] = (B_transport,topic_name)
        table[B_transport] = (A_transport,topic_name)
        
        # A와 B 에게 각자 상대 이름 보내주기 
        # partition 전송/수신 별로
        send_partition = "0"
        receive_partition = "1"
        msg_a = topic_name + "-" + send_partition    + "-" + receive_partition
        msg_b = topic_name + "-" + receive_partition + "-" + send_partition
        A_transport.write(msg_a.encode())
        B_transport.write(msg_b.encode())
        return 1
        
    
    def connectionMade(self):
        self._count += 1
        print("client connected!")
        transports.add(self.transport)
        waited_queue.append(self.transport)
        #유저이름추가
        users.add(str(self.transport))
        #self.transport.write("잠시만 기다려주세요")
        print("기다려주세요 매칭중입니다")
        self.matching()


    def dataReceived(self, data):
        for t in transports:
            if self.transport is not t:
                t.write(data)
    
    
    def connectionLost(self,reason):
        print(f"{self.transport}connections is Lost.. Bye")
        partner,topic = table.pop(self.transport)
        table.pop(partner)
        self.delete_topic(topic)
        print("TOPIC 삭제완료")

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()
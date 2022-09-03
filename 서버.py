#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 17:52:03 2022

@author: pn_jh
"""

from twisted.internet import protocol, reactor
import random
from collections import deque
names = ['##USER' + str(i) for i in range(10)]

transports = set()
partitions = set()
waited_queue = deque([])
users = set()

class Chat(protocol.Protocol):
    
    
    def produce_name_partition_number(self):
        name = ""
        for x in names:
            if x not in users:
                name = x
                break
        users.add(name)
        partition = 0 
        for i in range(10):
            if i not in partitions:
                partition = i 
                break
        partitions.add(partition)
        return name,partition
    
    def matching(self):
        A_transport,A_info = waited_queue.popleft()
        A_name,A_partition = A_info.split()
        
        B_transport,B_info = waited_queue.popleft()
        B_name,B_partition = B_info.split()
        msg_a = A_name + " " + A_partition + " " + B_partition
        msg_b = B_name + " " + B_partition + " " + A_partition
        A_transport.write(msg_a.encode())
        B_transport.write(msg_b.encode())
        
        return print(f" {A_name}-{A_partition }  와 {B_name}-{B_partition} 을 매칭시켰습니다 ")
    
    
    
    def connectionMade(self):
        print("client connected!")
        name,partition = self.produce_name_partition_number()
        transports.add(self.transport)
        client_info_msg = name + " " + str(partition)
        waited_queue.append((self.transport,client_info_msg))
        print("기다려주세요 매칭중입니다")
        if len(waited_queue) >= 2:
            self.matching()

    def dataReceived(self, data):
        for t in transports:
            if self.transport is not t:
                t.write(data)

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()

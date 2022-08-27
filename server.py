from twisted.internet import protocol, reactor
import random
from kafka import KafkaProducer
import json
from _collections import defaultdict
names = ['Mary','Cary','Bary','Dary','Arary','Movies1rary','Abiast']
COLORS = [
    '\033[31m', # RED
    '\033[32m', # GREEN
    '\033[33m', # YELLOW
    '\033[34m', # BLUE
    '\033[35m', # MAGENTA
    '\033[36m', # CYAN
    '\033[37m', # WHITE
    '\033[4m',  # UNDERLINE
]

transports = set()
users = set()
# 서버용 프로듀서 생성 ( 매칭 클라이언트에게 알려줄용도 )
server_producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],api_version = (0,10,1))
# protocol.Protocol 클래스 상속받고 오버라이딩 하기

waited_queue = []

class Chat(protocol.Protocol):



    def connectionMade(self):
        name = names[random.randint(0,len(names)-1)]
        color = COLORS[len(users) % len(COLORS)]
        users.add(name)
        waited_queue.append(name)
        transports.add(self.transport)
        if len(waited_queue) >= 2:
            a = waited_queue.pop()
            b= waited_queue.pop()
            # server_producer 를 이용하여 a 에게 b 의 아이디를 b에게는 a 아이디를 전송
            server_producer.send(a,json.dumps(b).encode('utf-8'))
            server_producer.send(b.json.dumps(a).encode('utf-8'))
        #print(self.transport)
        self.transport.write(f'{color}{name}\033[0m'.encode())

    def dataReceived(self, data):
        for t in transports:
            if self.transport is not t:
                t.write(data.encode())

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()

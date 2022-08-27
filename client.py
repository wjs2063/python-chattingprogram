import socket
import select
import sys
import json
from kafka import KafkaConsumer,KafkaProducer
import chardet
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

name = None
Audience = None
while True:
    read, write, fail = select.select((s, sys.stdin), (), ())

    for desc in read:
        if desc == s:
            data = s.recv(4096)
            print(data.decode())
            if name is None:

                name = data
                # 각 클라이언트마다 consumer, producer 생성
                print(type(name),len(name))
                print(chardet.detect(name.encode()))
                consumer = KafkaConsumer(name,
                                         bootstrap_servers=['localhost:9092'],
                                         api_version = (0,10)
                                         )
                producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],api_version = (0,10,1))
                print(" consumer,producer 생성이 완료되었습니다",name)
                s.send(f'{name} is connected!'.encode())

        else:
            if Audience == None:
                for message in consumer:
                    Audience = message.value.decode('utf-8-sig')
            text = ""

            msg = desc.readline()
            msg = msg.replace('\n', '')
            s.send(f'{name} {msg}'.encode())
            while text !="exit":
                text = input()
                producer.send(Audience,json.dumps(text).encode('utf-8-sig'))
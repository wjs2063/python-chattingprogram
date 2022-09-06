
## USAGE 

STEP 1

카프카폴더가있는 /Users/pn_jh/Desktop/개발/kafka/kafka_2.13-3.2.0 로 이동
Zookeeper 실행
```  
bin/zookeeper-server-start.sh config/zookeeper.properties   : Kafka 파일이 들어있는 폴더로 터미널 진입 후 지정 ( 상대경로이기때문) , 주키퍼실행
```

STEP 2

카프카 서버 실행
```
bin/kafka-server-start.sh config/server.properties           : Kafka 서버 실행
```

STEP 3

토픽생성
```
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --partitions 10 --replication-factor 1 --topic chat-kafka01
```

STEP 4

서버 소스코드 실행 

```
 python /Users/pn_jh/Desktop/개발/Kafka-realtime_chatting/chat_source/server.py
```
STEP 5
클라이언트 소스코드 실행 ( 터미널 여러개 띄워서 여러개 실행해야함)

```
python /Users/pn_jh/Desktop/개발/Kafka-realtime_chatting/chat_source/client.py
```



























## Error 

서버소켓에서 문자열을 주고받을때 byte 형식으로 주고받아서 type(name), len(name) 하면 str 길이는 13 이나오는 이상한 현상이발생한다 .

: 이유는 색깔을 입혀놓았기때문에 오류뜨는것이다 ㅎㅎ 색깔제거해주자

# python-chattingprogram
파이썬을 이용한 채팅프로그램


[목표]

서버 : 클라이언트가 접속하면 매칭해주고 관리하는 용도

Kafka : 서버로부터 매칭을받았으면 클라이언트마다 가지고있는

Prod1 ->  송신 -> Cons2 가 수신

Prod2 ->  송신 -> Cons1 가 수신 하는 방식으로 실시간 채팅메시지 시스템 구현 


토픽을 생성해야하는데 1인 1토픽은 메세지구독은 비현실적 이므로 partition 를 통하여 해결해보자

+ 비동기적으로 input 을 입력중에도 메세지는 도착해야한다 (스레드를 통해 해결, CPU 연산을 쓰지않는 I/O 연산이기때문에 thread 를 써도 무리없이 작동 할것이라고 생각)

-------------------------------------------------

카프카 브로커 내에 다수의 토픽 , 1개의 토픽 내에 다수의 파티션 ,

일단은 Consumer 가 특정 파티션만 구독 하도록 하고 , Prod 와 Cons 는 특정 파티션 에게만 송/수신을 하도록 구현
producer.send( partition = 내가원하는 partition ) 으로 특정 파티션에 전송하고 컨슈머는 특정 파티션만 구독하도록 설정할것 

consumer.assign([TopicPartition(TOPIC, 1)]) 와 같이 지정해주자 list 형식이고 꼭 TopicPartition() 이라는 함수를 써서 진행해야함

참고 [공식문서]
https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html?highlight=send#kafka.KafkaProducer.send


1. 그렇다면 몇개의 Topic 과 Partition 들을 구성을 해야하는가? 
2. 서버가 이름 + 파티션 까지 지정해주면 될것같다


----------------------------------------------------
# Error 및 중요한점 
참고 - https://kafka-python.readthedocs.io/en/2.0.1/apidoc/KafkaConsumer.html#kafka.KafkaConsumer.subscribe

### 특정 토픽의 특정 파티션만  구독하도록 설정하는것 !! 내가 원하는 메세지저장소와 흐름을 control 하는것이므로 중요하다. 
단 KafkaConsumer instance 생성시  TOPIC 구독 지정하지말자 -> 따로 지정
consumer.assign([TopicPartition(TOPIC, 1)]) 와 같이 지정해주자 list 형식이고 꼭 TopicPartition()

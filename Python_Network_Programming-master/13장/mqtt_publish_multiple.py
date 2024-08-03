# 다중 메시지 발행 프로그램

import paho.mqtt.publish as publish
broker = "test.mosquitto.org"

msgs = [{'topic':"mqtt/multiple", 'payload':"Hello"},
    ("mqtt/multiple", "World", 0, False)]
publish.multiple(msgs, hostname=broker)
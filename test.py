from mqtt import *
import time

# settings
s_mqtt_broker = "192.168.178.41"
s_mqtt_port = 1883


# mqtt listen function
def mqtt_recv(client, userdata, msg):
    # parse input
    timestamp = time.time()
    topic = msg.topic
    value = msg.payload.decode('utf-8')
    # queue.put([timestamp, topic, value])
    print(topic, msg.payload)

# create mqtt listener
mqtt_listener_all = MqttListener(s_mqtt_broker, s_mqtt_port, "#", mqtt_recv)

# loop
while True:
    time.sleep(1)

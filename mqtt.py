import paho.mqtt.client as mqtt
import json
import time
import sys

class MqttSender():
    def __init__(self, broker, port, topic, name):
        self.broker = broker
        self.port = port
        self.name = name
        
        # set topic
        if topic[-1] == "/":
            self.topic = '{}{}'.format(topic, self.name)
        else:
            self.topic = '{}/{}'.format(topic, self.name)

        self.connect()

    def connect(self):
        #TODO change to mac adress related name
        self.clientname = self.name + "_" + str(time.localtime().tm_min) + str(time.localtime().tm_sec)
        self.client = mqtt.Client(self.clientname)
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        rc = self.client.connect(self.broker, self.port)
        if rc == 0:
            print("[MQTT] connected to mqtt server {}:{} on {}".format(self.broker, self.port, self.topic))

    def send(self, payload, topic=""):
        payload = json.dumps(payload)
        if not topic == "":
            return self.client.publish(topic, payload)
        else:
            return self.client.publish(self.topic, payload)

    def on_publish(self, client, userdata, result):
        return result

    def on_disconnect(self, client, userdata, rc):
        print[f"[MQTT] disconnected: {str(rc)}"]
        print("[MQTT] trying to reconnect ...")
        self.client.reconnect()


class MqttListener():
    def __init__(self, broker, port, topic, function):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.function = function
        self.timeout = 10

        # create client object
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.connect()

    def connect(self):
        rc = self.client.connect(self.broker, self.port, self.timeout)
        if rc == 0:
            print("[MQTT] connectedn as listener to mqtt server {}:{} on {}".format(self.broker, self.port, self.topic))
            # start listening
            self.client.loop_start()
        else:
            print("[MQTT] error while disconne cting")

    def on_disconnect(self, client, userdata, rc):
        print[f"[MQTT] disconnected: {str(rc)}"]
        print("[MQTT] trying to reconnect ...")
        self.client.reconnect()
        
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)
        return rc

    def on_message(self, client, userdata, msg):
        self.function(client, userdata, msg)

if __name__ == "__main__":
    def on_msg(client, userdata, msg):
        print(msg.payload)

    listener = MqttListener("127.0.0.1", 1883, "test/#", on_msg)
    while input() != "q":
        pass

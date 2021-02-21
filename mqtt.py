import paho.mqtt.client as mqtt
import json

#ToDo: add general mqtt handler
#ToDo: add rules

class MqttSender():
    def __init__(self, broker, port, topic, name):
        self.broker = broker
        self.port = port
        self.name = name
        self.topic = topic
        
        # remove '/' if there
        if topic[-1] == "/":
            self.topic = self.topic[:-1]

        self.connect()

    def connect(self):
        #TODO change to mac adress related name
        self.client = mqtt.Client(self.name)
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker, self.port)
        print("[INFO] connected to mqtt server {}:{} on {} as sender: {}".format(self.broker, self.port, self.topic, self.name))

    def send(self, payload, topic="", name=""):
        payload = json.dumps(payload)
        if not topic == "":
            return self.client.publish('{}/{}'.format(topic, name), payload)
        else:
            return self.client.publish('{}/{}'.format(self.topic, self.name), payload)

    def on_publish(self, client, userdata, result):
        return result


class MqttListener():
    def __init__(self, broker, port, topic, name="*", function=None):
        self.broker = broker
        self.port = port
        self.name = name
        self.function = function

        # set topic
        if topic[-1] == "/":
            self.topic = '{}{}'.format(topic, self.name)
        else:
            self.topic = '{}/{}'.format(topic, self.name)

        self.connect()

    def on_message(self, client, userdata, msg):
        self.function(msg)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic)

    def connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

import paho.mqtt.client as mqtt
import socket
import json
import time
import sys

def get_ip_adress(timeout=10):
    ip = "0.0.0.0"
    counter = 0
    while ip == "0.0.0.0" and counter <= timeout:
        try:
            ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
            return ip
        except:
            print("[INFO] trying to connect to network..")
            time.sleep(1)
            counter += 1
    print("[ERROR] Timeout while trying to connect to network..")
    return None

def check_ip(ip, port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

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
        if not rc == 0: 
            print("[MQTT] connected to mqtt server {}:{} on {}".format(self.broker, self.port, self.topic))
        return rc

    def send(self, payload, topic=""):
        payload = json.dumps(payload)
        if not topic == "":
            rc = self.client.publish(topic, payload)
        else:
            rc = self.client.publish(self.topic, payload)
        if rc == 0:
            print("[MQTT] error while sending message.")
            print("[MQTT] maybe the client disconnected?")
        return rc

    def send_raw(self, payload, topic=""):
        if not topic == "":
            rc = self.client.publish(topic, payload)
        else:
            rc = self.client.publish(self.topic, payload)
        if rc == 0:
            print("[MQTT] error while sending message.")
            print("[MQTT] maybe the client disconnected?")
        return rc

    def on_publish(self, client, userdata, result):
        return result

    def on_disconnect(self, client, userdata, rc):
        print("[MQTT] trying to reconnect ...")
        self.client.reconnect()
        print("[MQTT] successfully reconnected")


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
            print("[MQTT] connected as listener to mqtt server {}:{} on {}".format(self.broker, self.port, self.topic))
            # start listening
            self.client.loop_start()
        else:
            print("[MQTT] error while connecting")

    def on_disconnect(self, client, userdata, rc):
        print(f"[MQTT] disconnected: {str(rc)}")
        print("[MQTT] trying to reconnect ...")
        self.client.reconnect()
        print("[MQTT] successfully reconnected")
        
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)
        return rc

    def on_message(self, client, userdata, msg):
        self.function(client, userdata, msg)

    def stop(self):
        self.client.loop_stop()

if __name__ == "__main__":
    def on_msg(client, userdata, msg):
        print(msg.payload)

    listener = MqttListener("127.0.0.1", 1883, "test/#", on_msg)
    while input() != "q":
        pass

import paho.mqtt.client as mqtt
import base64
import time

broker_address = "broker.hivemq.com"
broker_port = 1883
topic = "example_topic"

image: bytes

with open("./img.jpeg", "rb") as f:
    image = f.read()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

publisher = mqtt.Client("Publisher")
publisher.on_connect = on_connect

publisher.connect(broker_address, broker_port)
time.sleep(1)

message = base64.b64encode(image).decode("ascii")

while True:
    publisher.publish(topic, message)
    time.sleep(0.1)

publisher.disconnect()

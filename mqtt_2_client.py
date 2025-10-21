import paho.mqtt.client as mqtt
import time
import random

broker_adress="10.104.32.253"
broker_port=1883
topic="sensor/data"

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    temp,hum = map(float, payload.split(" "))
    print(f"Temperature={temp}°C, Humidity={hum}%")

client = mqtt.Client()
client.on_message = on_message
client.connect(broker_adress, broker_port)
client.subscribe(topic)
print(f"Topic subscription '{topic}' on broker {broker_adress}:{broker_port}")
client.loop_forever()

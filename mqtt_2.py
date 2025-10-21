import paho.mqtt.client as mqtt
import time
import random

broker_adress="10.104.32.253"
broker_port=1883
topic="sensor/data"

def read_sensor():
    return random.randint(500, 999)/10,random.randint(150,300)/10

def publish_data(client):
    temperature, humidity = read_sensor()
    if humidity is not None and temperature is not None:
        payload = f"{temperature:.2f} {humidity:.2f}"
        client.publish(topic, payload)
        print(f"Published: {payload}%")
    else:
        print("Failed to read from sensor")

client = mqtt.Client()
client.connect(broker_adress, broker_port, 60)
while True:
    publish_data(client)
    time.sleep(5)
    
    


import paho.mqtt.client as mqtt
import time
import random
import matplotlib.pyplot as plt

broker_adress="10.104.32.253"
broker_port=1883
topic_sensor="sensor/data"
topic_control="control/led"
temp_tab, hum_tab,time_tab = [], [], []

def publish_data(client,topic,message):
    payload = message
    client.publish(topic, payload)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    temp, hum = map(float, payload.split(" "))
    temp_tab.append(temp)
    hum_tab.append(hum)
    time_tab.append(time.time())
    if(temp>25):
        publish_data(client,topic_control,"ON")
    else:
        publish_data(client,topic_control,"OFF")
    plt.clf()
    plt.plot(time_tab, temp_tab, 'ro-', label='Temperature (°C)')
    plt.plot(time_tab, hum_tab, 'bo-', label='Humidity (%)')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.draw()
    plt.pause(0.01)



plt.ion()
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_adress, broker_port)
client.subscribe(topic_sensor)
print(f"Topic subscription '{topic_sensor}' on broker {broker_adress}:{broker_port}")
client.loop_start()

while True:
    plt.pause(0.1)
    time.sleep(0.1)


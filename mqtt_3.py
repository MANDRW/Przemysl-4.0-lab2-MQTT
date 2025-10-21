import paho.mqtt.client as mqtt
import time
import random
import RPi.GPIO as GPIO
import pigpio 

def on_led(gpio):
    GPIO.output(gpio,GPIO.HIGH) 

def off_led(gpio):
    GPIO.output(gpio,GPIO.LOW )

def read_sensor():
    return random.randint(150,300)/10

def publish_data(client,temp):
    temperature=temp 
    humidity = read_sensor()
    if humidity is not None and temperature is not None:
        payload = f"{temperature:.2f} {humidity:.2f}"
        client.publish(topic_sensor, payload)
        print(f"Published: {payload}%")
    else:
        print("Failed to read from sensor")

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(payload)
    if(payload=="OFF"):
        off_led(19)
    if(payload=="ON"):
        on_led(19)
    

    

broker_adress="10.104.32.253"
broker_port=1883
topic_sensor="sensor/data"
topic_control="control/led"

led_pin=19
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)
off_led(led_pin)

pi=pigpio.pi()
if not pi.connected:
    exit(0)

sensor=pi.spi_open(1,1000000,0)
stop=time.time()+600



client = mqtt.Client()
client.on_message=on_message


client.connect(broker_adress, broker_port, 60)
client.subscribe(topic_control)
client.loop_start()

try:
    while True:
        c,d=pi.spi_read(sensor,2)
        if c==2:
            sign=(d[0]&0x80)>>7
            value=(((d[0]&0x7f)<<8)|d[1])>>5
            temp=value*0.125
            if sign==1:
                temp=temp* -1
            publish_data(client,temp)
            time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()
    pi.spi_close(sensor)
    pi.stop()


    
    


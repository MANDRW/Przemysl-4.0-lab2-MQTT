import RPi.GPIO as GPIO 
import time
import pigpio 

leds=[19,18,13,12]


def on_led(gpio):
    GPIO.output(gpio,GPIO.HIGH) 

def off_led(gpio):
    GPIO.output(gpio,GPIO.LOW )

def change_led_state(gpio):
    if(GPIO.input(gpio)==1):
        off_led(gpio)
    else:
        on_led(gpio)

def led_term(temp):
    if(temp>25.0):
        on_led(leds[3])
    else:
        off_led(leds[3])
    if(temp>26.0):
        on_led(leds[2])
    else:
        off_led(leds[2])
    if(temp>27.0):
        on_led(leds[1])
    else:
        off_led(leds[1])
    if(temp>28.0):
        on_led(leds[0])
    else:
        off_led(leds[0])


if __name__ == "__main__" :
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    

    pi=pigpio.pi()
if not pi.connected:
    exit(0)

sensor=pi.spi_open(1,1000000,0)
stop=time.time()+600

while time.time()<stop:
    c,d=pi.spi_read(sensor,2)
    if c==2:
        sign=(d[0]&0x80)>>7
        value=(((d[0]&0x7f)<<8)|d[1])>>5
        temp=value*0.125
        if sign==1:
            temp=temp* -1
        print("{:.2f}".format(temp))
        led_term(temp)
    time.sleep(0.25)
pi.spi_close(sensor)
pi.stop()

    
GPIO.cleanup()
import RPi.GPIO as GPIO
import time
sensor = 16
Led = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(Led, GPIO.OUT)
GPIO.output(Led,False)
while True:
    if(GPIO.input(sensor)==False):
        GPIO.output(Led,True)
        print("Object Found")
        time.sleep(1)
    else:
        GPIO.output(Led,False)
        print("No Object Found")
        time.sleep(1)
    
 
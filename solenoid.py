def unlock_solenoid():
    import RPi.GPIO as GPIO
    from time import sleep

    RELAY_PIN = 11

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    
    print("Execution")
    GPIO.output(RELAY_PIN, 0)
    sleep(5)
    GPIO.output(RELAY_PIN, 1)
    
            
    GPIO.cleanup()
#unlock_solenoid()


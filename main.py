import camera  # to import the camera file that we have
import working_telegramBot as T_B
import facerecog as fg
import RPi.GPIO as GPIO
import time
import RPi_I2C_driver
import solenoid as SL

sensor = 16
#Led = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)
mylcd = RPi_I2C_driver.lcd()
# mylcd.lcd_clear();
# mylcd.backlight(0)
#GPIO.setup(Led, GPIO.OUT)
#GPIO.output(Led,False)
while True:
    if(GPIO.input(sensor)==False):
        #GPIO.output(Led,True)
        mylcd.lcd_clear();
        mylcd.backlight(0)
        print("Someone is at the Door")
        
        # test 2
        mylcd.lcd_display_string("Hello..!", 1)
        mylcd.lcd_display_string("Please wait...", 2)
        time.sleep(3)
        mylcd.lcd_clear()
        
        mylcd.lcd_display_string("Stand still...", 1)
        mylcd.lcd_display_string("Capturing photo", 2)
        time.sleep(2)
        camera.new_camera()
        time.sleep(1)
        mylcd.lcd_clear()
        
        mylcd.lcd_display_string("Stand still...", 1)
        mylcd.lcd_display_string("Capturing video", 2)
        camera.video_function()
        time.sleep(1)
        mylcd.lcd_clear()
        mylcd.backlight(0)
        
        found = fg.face_rec("test0.jpg")
#         found = 0
        if not found:
            mylcd.lcd_display_string("Face Not", 1)
            mylcd.lcd_display_string("Recognised!!", 2)
            time.sleep(2)
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Please Wait!!", 1)
            T_B.telegram_notify()
        else:
            SL.unlock_solenoid()
            
        time.sleep(1)
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(sensor, GPIO.IN)
        mylcd.lcd_clear();
        mylcd.backlight(0)
        #GPIO.setup(Led, GPIO.OUT)
        #GPIO.output(Led,False)
        
        
    else:
#         mylcd.lcd_clear();
#         mylcd.backlight(0)
        #GPIO.output(Led,False)
        print("No One is at the Door")
        time.sleep(1)
    
 
 
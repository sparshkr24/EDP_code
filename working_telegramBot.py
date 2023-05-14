response_received = False
import solenoid as SL
import RPi_I2C_driver
from time import *
import lcd

latest_update_id = 0
def telegram_notify():
    import json
    import requests
    import sys

    token = "6027992942:AAHDHEFjpDpjnRCJ3cIBU4RqGkVkGDbVKD8"
    chat_id = 1231120196  # chat id

    image = "test0.jpg"
    message = "Someone is at the door..."
    

    url_pic = f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={message}"

    files = {}
    files["photo"] = open(image, "rb")
    requests.get(url_pic, params={"chat_id": chat_id}, files=files)

    data = {
        "chat_id": chat_id,
        "text": "Select an option",
        "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": "Lock", "callback_data": "/lock"}],
                    [{"text": "Unlock", "callback_data": "/unlock"}]
                ],
            'resize_keyboard': True
        })
    }

    # Send the message to the Telegram API
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data=data)


    def lock_door():
        print("Door locked function called")
        mylcd = RPi_I2C_driver.lcd()
        # test 2
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Sorry..!", 1)
        mylcd.lcd_display_string("Access Denied", 2)

        sleep(5)

        mylcd.lcd_clear()
        mylcd.backlight(0)
        


    def unlock_door():
        # Code to unlock the door goes here
        print("Door unlocked function called")
        mylcd = RPi_I2C_driver.lcd()
        mylcd.lcd_clear()
        # test 2
        mylcd.lcd_display_string("Welcome..!", 1)
        mylcd.lcd_display_string("Door unlocked", 2)
        SL.unlock_solenoid()
        sleep(1) # 2 sec delay

        mylcd.lcd_clear()
        lcd.smiley()
        mylcd.backlight(0)
        


    def handle_callback_query(callback_query):
        global response_received
        message = ""
        query_data = callback_query["data"]
        if query_data == "/lock":
            lock_door()
            message = "Door locked"
        elif query_data == "/unlock":
            unlock_door()
            message = "Door unlocked"

        response_received = True

        # Answer the callback query to remove the "pending" state
        callback_query_id = callback_query["id"]
        url = f"https://api.telegram.org/bot{token}/answerCallbackQuery?callback_query_id={callback_query_id}"
        requests.get(url)

        # Send a message to the chat to indicate the door is locked/unlocked
        data = {
            "chat_id": chat_id,
            "text": message
        }
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data=data)


    def handle_updates():
        # Use the global variable to keep track of the latest update ID
        global latest_update_id, response_received

        url = f"https://api.telegram.org/bot{token}/getUpdates?offset={latest_update_id + 1}"

        response = requests.get(url)
        json_response = response.json()

        file1 = open("old_id.txt", "r")
        old_id = int(file1.read())
        if (json_response['result']):
            new_id = json_response['result'][-1]['update_id']
        else:
            new_id = 0

        # print(json_response["result"])
        if json_response["ok"] and json_response["result"]:
            if "callback_query" in json_response["result"][-1] and new_id > old_id:
                str1 = str(new_id)
                file1.close()
                file2 = open("old_id.txt", "w+")
                file2.write(str1)
                file2.close()
                callback_query = json_response["result"][-1]["callback_query"]
                # print(json_response["result"][-1]["callback_query"])
                handle_callback_query(callback_query)
                # Update the latest update ID
                latest_update_id = json_response["result"][-1]["update_id"]


    while True:
        global response_received
        handle_updates()
        if response_received:  # Exit loop once a response has been received
            response_received = False
            break


# telegram_notify()


import RPi.GPIO as GPIO
import time
import os
import requests

GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
LED_PIN = 18
GPIO.setwarnings(False)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

signal = 0 # cam
count = 0 # cam once

url = "http://118.67.130.241:8080/rpi/pir"

try:
    print("PIR module test (CTRL+C to exit)")
    time.sleep(2)
    print("ready")

    while True:
        if GPIO.input(PIR_PIN)==GPIO.HIGH:
            t = time.localtime()
            print("%d:%d:%d  Yes" % (t.tm_hour, t.tm_min, t.tm_sec))
            GPIO.output(LED_PIN, True)

            signal = True

            pir_data = {
                'pir' : signal
            }
            headers = {'Content-Type':'application/json; charset=utf-8'}
            cookies = {'pir_cookie':'pir_cookies'}
            os.system("sudo service motion start")
            
            response = requests.post(url, json=pir_data, headers=headers, cookies=cookies)
            
            face_signal = response.json()['face_signal']
            print(face_signal)
            
            if(face_signal==True):
                signal = False
                os.system("sudo service motion stop")
            else:
                signal = False
                os.system("sudo service motion stop")
                
        else:
            print("nonononono")
            GPIO.output(LED_PIN, False) 

        time.sleep(0.5)
    

except KeyboardInterrupt:
    print("quit")
    GPIO.cleanup()

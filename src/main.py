from machine import Pin
import time
import socket
import os

import wifi
import webserver
import config


led = Pin(2, Pin.OUT)
SSID="ASUS_28_2G"
PASSWORD="88483306"
AP_SSID = 'esp32-sunlight'
AP_PASSWORD = '123456789'


try:
    config.read_config_file()
    print(config.config)
    print(os.listdir())
    #os.remove("config.txt")

    if(wifi.connectWifi(config.config["ssid"],config.config["password"])):           
        print("WIFI !")
        led.value(1)
    else:
        print("no wifi :(")
        led.value(0)
        wifi.createHotspot(AP_SSID,AP_PASSWORD)

    webserver.app.run(debug=True, host = "", port=80)    
except Exception as e:
    print(e)
    wifi.closeWifi()

from machine import Pin
import neopixel
import time
import socket
import os

import wifi
import webserver
import config
import utime

# LEDs
pixels = 37
led_pin = 5
pixel_strip = None

# Button
btn_up_pin = 4
btn_down_pin = 2
intTimeUp = 0
intTimeDown = 0
intTimeMid = 0
debTime = 100
lastPos = ""
btn_up = None
btn_down = None
ON = 1
OFF = 0

# Network
SSID="ASUS_28_2G"
PASSWORD="88483306"
AP_SSID = 'esp32-sunlight'
AP_PASSWORD = '123456789'

def main():
    try:
        config.read_config_file()
        print(config.config)
        print(os.listdir())
        #os.remove("config.txt")

        initialize_button_led()
        wifi.initializeNetwork()
        webserver.app.run(debug=True, host = "", port=80)    
    except Exception as e:
        print(e)
        wifi.closeWifi()

def initialize_button_led():
    global btn_up
    global btn_down
    global pixel_strip

    # LEDs
    pixel_strip = neopixel.NeoPixel(Pin(led_pin), pixels)
    for i in range(pixels):
        pixel_strip[i] = (0, 0, 0)
    pixel_strip.write()

    # Button
    btn_down = Pin(btn_down_pin, Pin.OUT, value=ON)    
    btn_down.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)
    btn_up = Pin(btn_up_pin, Pin.OUT, value=ON)    
    btn_up.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)
    print(btn_down.value())
    print(btn_up.value())

def button_handler(pin):
    global intTimeUp
    global intTimeMid
    global intTimeDown
    global btn_up
    global btn_down
    global lastPos
    if btn_up.value() == ON and btn_down.value() == OFF:
        if lastPos != "UP" and utime.ticks_diff(utime.ticks_ms(), intTimeUp) > debTime:
            print("UP")
            for i in range(pixels):
                pixel_strip[i] = (10, 0, 10)
            pixel_strip.write()
            lastPos = "UP"
            intTimeUp = utime.ticks_ms()
    elif btn_down.value() == ON and btn_up.value() == OFF:
        if lastPos != "DOWN" and utime.ticks_diff(utime.ticks_ms(), intTimeDown) > debTime:
            print("DOWN")
            for i in range(pixels):
                pixel_strip[i] = (10, 10, 0)
            pixel_strip.write()
            lastPos = "DOWN"
            intTimeDown = utime.ticks_ms()
    elif btn_up.value() == ON and btn_down.value() == ON:
        if lastPos != "MID" and utime.ticks_diff(utime.ticks_ms(), intTimeMid) > debTime:
            print("MIDDLE")
            for i in range(pixels):
                pixel_strip[i] = (0, 0, 0)
            pixel_strip.write()
            lastPos = "MID"
            intTimeMid = utime.ticks_ms()

main()
from machine import Pin
import neopixel
import time
import socket
import os

import wifi
import webserver
import config
import utime

n = 37
p = 5

np = neopixel.NeoPixel(Pin(p), n)

for i in range(n):
    np[i] = (0, 0, 0)
np.write()

intTimeUp = 0
intTimeUpMid = 0
intTimeDown = 0
intTimeDownMid = 0
intTimeMid = 0
debTime = 100
lastPos = ""
ON = 1
OFF = 0

def button_handler_up(pin):
  global intTimeUp
  global intTimeUpMid
  if pin.value() == ON:
    if utime.ticks_diff(utime.ticks_ms(), intTimeUp) > debTime:
      print("UP")
      for i in range(n):
          np[i] = (10, 0, 10)
      np.write()
    intTimeUp = utime.ticks_ms()
  else:
    if utime.ticks_diff(utime.ticks_ms(), intTimeUpMid) > debTime:
      print("MIDDLE")
      for i in range(n):
          np[i] = (0, 0, 0)
      np.write()
    intTimeUpMid = utime.ticks_ms()

def button_handler_down(pin):  
  global intTimeDown
  global intTimeDownMid
  if pin.value() == ON:
      if utime.ticks_diff(utime.ticks_ms(), intTimeDown) > debTime:
        print("DOWN")
        for i in range(n):
            np[i] = (10, 10, 0)
        np.write()        
        intTimeDown = utime.ticks_ms()
  else:
    if utime.ticks_diff(utime.ticks_ms(), intTimeDownMid) > debTime:
      print("MIDDLE")
      for i in range(n):
          np[i] = (0, 0, 0)
      np.write()
    intTimeDownMid = utime.ticks_ms()
  
def button_handler(pin):
    global intTimeUp
    global intTimeMid
    global intTimeDown
    global btn_up
    global btn_down
    global lastPos
    
    #print(btn_up.value())
    #print(btn_down.value())
    if btn_up.value() == ON and btn_down.value() == OFF:
        if lastPos != "UP" and utime.ticks_diff(utime.ticks_ms(), intTimeUp) > debTime:
            print("UP")
            for i in range(n):
                np[i] = (10, 0, 10)
            np.write()
            lastPos = "UP"
            intTimeUp = utime.ticks_ms()
    elif btn_down.value() == ON and btn_up.value() == OFF:
        if lastPos != "DOWN" and utime.ticks_diff(utime.ticks_ms(), intTimeDown) > debTime:
            print("DOWN")
            for i in range(n):
                np[i] = (10, 10, 0)
            np.write()
            lastPos = "DOWN"
            intTimeDown = utime.ticks_ms()
    elif btn_up.value() == ON and btn_down.value() == ON:
        if lastPos != "MID" and utime.ticks_diff(utime.ticks_ms(), intTimeMid) > debTime:
            print("MIDDLE")
            for i in range(n):
                np[i] = (0, 0, 0)
            np.write()
            lastPos = "MID"
            intTimeMid = utime.ticks_ms()

btn_down = Pin(2, Pin.OUT, value=1)
#btn_down.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler_down)
btn_down.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)
btn_up = Pin(4, Pin.OUT, value=1)
#btn_up.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler_up)
btn_up.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)
#btn_down.value(0)
#btn_up.value(0)

print(btn_down.value())
print(btn_up.value())

SSID="ASUS_28_2G"
PASSWORD="88483306"
AP_SSID = 'esp32-sunlight'
AP_PASSWORD = '123456789'

try:
    config.read_config_file()
    print(config.config)
    print(os.listdir())
    #os.remove("config.txt")

    wifi.initializeNetwork()
    webserver.app.run(debug=True, host = "", port=80)    
except Exception as e:
    print(e)
    wifi.closeWifi()

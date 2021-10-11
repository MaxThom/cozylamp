import socket
import network
import time
from machine import Pin


host='192.168.3.147'
port = 10000

MAX_WAIT_SEC = 10
wlan=None
s=None

def connectWifi(ssid,passwd):
  global wlan
  try:
    wlan=network.WLAN(network.STA_IF)                 #create a wlan object
    wlan.active(True)                                 #Activate the network interface
    wlan.disconnect()                                 #Disconnect the last connected WiFi
    wlan.connect(ssid,passwd)                         #connect wifi
    
    
    wait_cycle = 0
    while(wlan.ifconfig()[0]=='0.0.0.0'):
      time.sleep(1)
      wait_cycle = wait_cycle + 1
      if wait_cycle >= MAX_WAIT_SEC:
        return False
    print(wlan.ifconfig())
    return True
  except:
    return False
  
def closeWifi():
  if (s):
    s.close()
  wlan.disconnect()
  wlan.active(False)

def createHotspot(ssid,password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while not ap.active():
        pass
    print('network config:', ap.ifconfig())
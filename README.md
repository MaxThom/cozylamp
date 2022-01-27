# cozylamp
Cozy lamp project using ESP32 and micropython

https://icircuit.net/make-esp32-http-webserver-using-micropython/2152
https://techtutorialsx.com/2017/09/06/esp32-micropython-serving-html-from-the-file-system-in-picoweb/
https://www.cnx-software.com/2017/10/16/esp32-micropython-tutorials/
https://github.com/pfalcon/picoweb

# you must upload the project first to use wifi, else import network
import wifi
wifi.connectWifi("NetComm 3296", "Huqupihuwo")
import upip
upip.install('picoweb')
upip.install('pycopy-ulogging')
upip.install('urequests')
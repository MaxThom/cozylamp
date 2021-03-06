from machine import Pin
import neopixel
import config
import utime
import time
import _thread

# LEDs
pixels = 37
led_pin = 5 #2
pixel_strip = None
pixel_pin = Pin(led_pin)

# Button
btn_up_pin = 4 #23
btn_down_pin = 2 #22
intTimeUp = 0
intTimeDown = 0
intTimeMid = 0
debTime = 100
lastPos = ""
btn_up = None
btn_down = None
ON = 1
OFF = 0
brightness = 0.5

def set_light_on():
    color = hex_to_rgb(config.config[config.status["color"]])
    print(color)
    set_color(color)

def set_light_off():
    set_color((0, 0, 0))

def set_color(color):
    #for i in range(pixels):
    #    pixel_strip[i] = color
    pixel_strip.fill(color)
    pixel_strip.write()
    pixel_pin.off()
    #time.sleep_us(300)

def on_button_up():
    global brightness
    config.status["light"] = "💡"
    brightness = 1
    set_light_on()

def on_button_mid():
    global brightness
    config.status["light"] = "💡"
    brightness = 0.5
    set_light_on()

def on_button_down():
    config.status["light"] = "off"
    set_light_off()

def initialize_io():
    print("Initializing io ...")
    global btn_up
    global btn_down
    global pixel_strip
    global pixel_pin

    # LEDs
    pixel_strip = neopixel.NeoPixel(pixel_pin, pixels)
    set_light_off()

    # Button
    btn_down = Pin(btn_down_pin, Pin.OUT, value=ON)
    btn_down.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)
    btn_up = Pin(btn_up_pin, Pin.OUT, value=ON)
    btn_up.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)
    button_handler(None)

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
            lastPos = "UP"
            intTimeUp = utime.ticks_ms()
            on_button_up()
    elif btn_down.value() == ON and btn_up.value() == OFF:
        if lastPos != "DOWN" and utime.ticks_diff(utime.ticks_ms(), intTimeDown) > debTime:
            print("DOWN")
            lastPos = "DOWN"
            intTimeDown = utime.ticks_ms()
            on_button_down()
    elif btn_up.value() == ON and btn_down.value() == ON:
        if lastPos != "MID" and utime.ticks_diff(utime.ticks_ms(), intTimeMid) > debTime:
            print("MIDDLE")
            lastPos = "MID"
            intTimeMid = utime.ticks_ms()
            on_button_mid()

def hex_to_rgb(clr):
    global brightness
    value = clr.lstrip('#')
    lv = len(value)
    color = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    color = tuple(int(brightness * x) for x in color)
    return color
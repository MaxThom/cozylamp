import urequests
import config
import time
import io

STATUS_SEC = 5

def updateStatus():
    print("Initializing request ...")
    while True:
        if config.status["light"] == "💡":
            try:
                print(f"{config.config['url']}/api/updatestatus/{config.config['device_key']}/{config.config['group_key']}")
                response = urequests.get(f"{config.config['url']}/api/updatestatus/{config.config['device_key']}/{config.config['group_key']}")
                values = response.json()
                print(values)

                if len(values) == 0:
                    config.status["color"] = "on_color"
                else:
                    config.status["color"] = "thinking_color"

                if config.status["light"] == "💡":
                    io.set_light_on()

                #print(response.status_code)
                #print(response.reason)
                response.close()
                config.status["server"] = "connected 🟢"
            except Exception as e:
                print(f"Request error: \n{e}")
                config.status["server"] = "disconnected 🔴"
        time.sleep(STATUS_SEC)

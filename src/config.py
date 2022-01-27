import json

config = {
    "ssid": "",
    "password": "",
    "url": "",
    "group_key": "",
    "device_key": "",
    "on_color": "",
    "thinking_color": ""
}

status = {
    "network": "",
    "server": "diconnected 🔴",
    "light": "",
    "color": "on_color"
}

def write_config_file():
    global config
    with open("config.txt", 'w') as fp:
        json.dump(config, fp)

def read_config_file():
    global config
    try:
        with open("config.txt") as fp:
            config = json.load(fp)
    except:
        set_factory_config()

def set_factory_config():
    global config
    config = {
        "ssid": "",
        "password": "",
        "url": "",
        "group_key": "",
        "device_key": "",
        "on_color": "#feffb3",
        "thinking_color": "#e100ff"
    }
    write_config_file()
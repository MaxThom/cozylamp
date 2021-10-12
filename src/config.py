import json

config = {
    "ssid": "",
    "password": ""
}

status = {
    "network": "",
    "server": "connected 🟢🔴"
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
        "password": ""
    }
    write_config_file()
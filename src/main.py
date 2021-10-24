import os
import _thread

import wifi
import webserver
import config
import io
import request


def main():
    try:
        config.read_config_file()
        print(config.config)
        #print(os.listdir())
        #os.remove("config.txt")

        io.initialize_io()
        wifi.initializeNetwork()
        _thread.start_new_thread(request.updateStatus, ())
        
        webserver.app.run(debug=True, host = "", port=80)            
    except Exception as e:
        print(e)
        wifi.closeWifi()

main()
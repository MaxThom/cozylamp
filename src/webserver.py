import picoweb
import config
import time
import wifi

app = picoweb.WebApp(__name__)
 
@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(f"""\
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>The cozy lamp 🕯️</title>
  </head>
  <body>
    <h1>The cozy lamp🕯️</h1>
    <h3>Wifi settings</h3>
    
    <form action='wifi_form' method='POST'>
        <strong>SSID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong> <input name='ssid' value='{config.config["ssid"]}'/></br>
        <strong>Password</strong> <input name='password' value='{config.config["password"]}'/></br>
        <ul>
          <li><i>blue led mean board is connected to wifi</i></li>
          <li><i>no blue led mean board is in hotspot mode</i></li>
        </ul>
        
        </br>
        <input type='submit'>
    </form>
  </body>
</html> 
""")
 
@app.route("/wifi_form")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  
        req.parse_qs()

    yield from picoweb.start_response(resp)
    yield from resp.awrite("""\
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>The cozy lamp 🕯️</title>
  </head>
  <body>
    <h1>The cozy lamp🕯️</h1>
    <h3>Your settings has been changed !</h3>
    <p>&nbsp;&nbsp;&nbsp;redirecting to settings in <span id="redirect">3</span> sec...</p>
  </body>
   <script>
      var timer = 2
      setTimeout(function(){
          window.location.href = '/';
        }, 3000);
      var x = setInterval(function() {
        document.getElementById("redirect").innerHTML = timer
        timer = timer - 1
      }, 1000);
   </script>
</html> 
""")
    time.sleep(2)
    if config.config["ssid"] != req.form['ssid'] or config.config["password"] != req.form['password']:
      config.config["ssid"] = req.form['ssid']
      config.config["password"] = req.form['password']   
      wifi.initializeNetwork()
     
    config.write_config_file()
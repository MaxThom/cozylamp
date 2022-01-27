import picoweb
import config
import time
import wifi
import io

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
    <h3>Status</h3>
      <span><strong>Network:</strong> {config.status["network"]}</span></br>
      <span><strong>Server:</strong> {config.status["server"]}</span></br>
      <span><strong>Light:</strong> {config.status["light"]}</span>
    <form action='settings_form' method='POST'>
      <h3>Color settings</h3>
      <div>
        <strong>On&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong>
        <input type="color" id="on_color" name="on_color" value="{config.config["on_color"]}"></br>
        <strong>Thinking of you</strong>
        <input type="color" id="thinking_color" name="thinking_color" value="{config.config["thinking_color"]}"></br>
      </div>

      <h3>Wifi settings</h3>
        <strong>SSID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong> <input name='ssid' value='{config.config["ssid"]}'/></br>
        <strong>Password</strong> <input name='password' value='{config.config["password"]}'/></br>
        </br>

      <h3>Lamp settings</h3>
        <strong>Server Url&nbsp;</strong> <input name='url' value='{config.config["url"]}'/></br>
        <strong>Group Key</strong> <input name='group_key' value='{config.config["group_key"]}'/></br>
        <strong>Device Key</strong> <input name='device_key' value='{config.config["device_key"]}'/></br>
        </br>

      <input type='submit'>
    </form>
  </body>
</html>
""")

@app.route("/settings_form")
def form_after(req, resp):
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

    config.config["url"] = req.form['url']
    config.config["group_key"] = req.form['group_key']
    config.config["device_key"] = req.form['device_key']
    config.config["on_color"] = req.form['on_color']
    config.config["thinking_color"] = req.form['thinking_color']
    config.write_config_file()

    if config.status["light"] == "💡":
      io.set_light_on()

#@app.route("/favicon.ico")
#def favicon(req, resp):
#  yield from app.sendfile(resp, "favicon.ico")
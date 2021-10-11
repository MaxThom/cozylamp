import picoweb
import config
import time
 
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
        </br>
        <input type='submit'>
    </form>
  </body>
</html> 
""")
    

    #htmlFile = open('index.html', 'r')
    #for line in htmlFile:
    #  yield from resp.awrite(line)
 
@app.route("/wifi_form")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        # Note: parse_qs() is not a coroutine, but a normal function.
        # But you can call it using yield from too.
        req.parse_qs()

    # Whether form data comes from GET or POST request, once parsed,
    # it's available as req.form dictionary

    msg= f"{req.form['ssid']}///{req.form['password']}"
    config.config["ssid"] = req.form['ssid']
    config.config["password"] = req.form['password']
    

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
    <h3>Your settings has been changed !</h3>
    <p>&nbsp;&nbsp;&nbsp;rebooting device in 5 sec...</p>
  </body>
</html> 
""")
    time.sleep(3)
    config.write_config_file()
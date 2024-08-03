from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import RPi.GPIO as GP
import sys
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
#Data pin is connected to GPIO3(pin=5)
GPIOpin = 3

def TempHum():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIOpin)
        print("Temp = {:0.1f}C Humidity = {:0.1f}".format(temperature, humidity))
        return temperature, humidity
        #time.sleep(3)

#items = {"led", "motor", "sensor", "lamp"}

def query_parse(query):
        a = query.split("&")
        temp = []
        for item in a:
            temp.append(item.split("="))
        for i in range(len(temp)):
            if len(temp[i]) == 1:
                temp[i].append('')
        
        return dict(temp)

def setGPIO(pin, mode):
        GP.setmode(GP.BCM)
        GP.setwarnings(False)
        GP.setup(pin, mode)
    
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        msg = parsed_path.query
        if msg == '':
            return
        parsed_query = query_parse(msg)
        
        if parsed_query["led"] == "on":
                resp="LED is ON"
                GP.output(18, 1)
        elif parsed_query["led"] == "off":
                resp="LED is OFF"
                GP.output(18, 0)
        else:
                resp="Fault"

        if "switch" in parsed_query.keys():
                GP.setup(23, GP.IN)
                state = GP.input(23)
                if state == 0:
                        resp = "Switch is OFF"
                else:
                        resp = "Switch is ON"
        if "temphud" in parsed_query.keys():
                (t, h) = TempHum()
                resp = "Temperature is {}C and Humidity is {}%".format(t, h)

        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(resp.encode())


setGPIO(18, GP.OUT)

httpd = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()

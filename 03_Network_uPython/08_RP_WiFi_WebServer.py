import machine
import time
import network
import socket

led_onboard = machine.Pin('LED', machine.Pin.OUT)
ssid = "DDTSW_Classroom_1"
password = "11111111"

def wifi_disconnect():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print("Disconnecting from network...")
        wlan.disconnect()
        while wlan.isconnected():
            time.sleep_ms(100)
        print("Disconnected from network")

def wifi_connect():
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True) 

    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(ssid, password)  

        while not wlan.isconnected():
            led_onboard.toggle()
            time.sleep_ms(100)

        print(f"Connected to {ssid} successfully!")
        print('Network Config :', wlan.ifconfig())
        led_onboard.value(1)
        return True
    else:
        print("Already connected to network:", wlan.ifconfig())
        return True


def web_page():
    if led_onboard.value() == 0:
        gpio_state="OFF"
    else:
        gpio_state="ON"
  
    html = """<html><head> <title>PICO LED control</title> <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
        .button2{background-color: #4286f4;}</style></head><body> <h1>PICO LED control</h1> 
        <p>LED state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
        <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
    return html

if __name__=="__main__":
    wifi_disconnect()
    if wifi_connect():
        my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        my_socket.bind(('', 80))
        my_socket.listen(5)
        
        while True:
            client, addr = my_socket.accept()
            print('connection from %s' % str(addr))
            request = client.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            led_on = request.find('/?led=on')
            led_off = request.find('/?led=off')
            if led_on == 6:
                print('LED ON')
                led_onboard.value(1)
            if led_off == 6:
                print('LED OFF')
                led_onboard.value(0)
            response = web_page()
            client.send('HTTP/1.1 200 OK\n')
            client.send('Content-Type: text/html\n')
            client.send('Connection: close\n\n')
            client.sendall(response)
            client.close()

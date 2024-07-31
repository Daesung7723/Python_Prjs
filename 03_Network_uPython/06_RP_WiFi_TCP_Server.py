import machine
import network
import time
import usocket as socket
import _thread as thread

led_onboard = machine.Pin('LED', machine.Pin.OUT)
ssid = "U+Net3808"
password = "952975#94P"
server_port = 12345  # TCP Server Port No.

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

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received data:", data.decode('utf-8'))
            # time.sleep_ms(1)
        except Exception as e:
            print("Error:", e)
            break
    client_socket.close()

def main():
    if wifi_connect():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', server_port))
        server_socket.listen(1)  # Max. 1 - RP Pico W has 2 Cores

        print("TCP server started on port", server_port)

        while True:
            try:
                client_socket, addr = server_socket.accept()
                print("Accepted connection from", addr)
                thread.start_new_thread(handle_client, (client_socket,))
                response = "<RP_PI_PICO TCP Server!>"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()

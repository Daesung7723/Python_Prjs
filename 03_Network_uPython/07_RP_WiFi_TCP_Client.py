import machine
import network
import usocket as socket
import time

led_onboard = machine.Pin('LED', machine.Pin.OUT)
ssid = "U+Net3808"
password = "952975#94P"

server_ip = "192.168.219.140"
server_port = 23

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

def main():
    if wifi_connect():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_addr = (server_ip, server_port)
            client_socket.connect(server_addr)
            print("Connected to server")

            while True:
                data_to_send = "Hello, Server!"
                client_socket.send(data_to_send.encode('utf-8'))
                print("Sent data:", data_to_send)

                data_received = client_socket.recv(1024)
                if data_received:
                    print("Received data:", data_received.decode('utf-8'))

                # time.sleep(1)

        except Exception as e:
            print("Error:", e)
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()

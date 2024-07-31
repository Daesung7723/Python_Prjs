import machine
import network
import time

led_onboard = machine.Pin('LED', machine.Pin.OUT)
ssid = "Mffice_1"
password = "mfficegg"
static_ip = "192.168.137.150"  # Static IP
subnet_mask = "255.255.255.0"  # Subnet Mask
gateway = "192.168.137.1"  # Gateway
dns_server = "8.8.8.8"  # DNS Server

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.active(True)        
        wlan.ifconfig((static_ip, subnet_mask, gateway, dns_server))  # IP Address Set
        wlan.connect(ssid, password)  # WiFi Connecting
        
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

if wifi_connect():
    pass
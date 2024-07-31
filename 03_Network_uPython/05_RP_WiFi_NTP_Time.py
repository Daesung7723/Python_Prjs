import machine
import network
import time
import ntptime

led_onboard = machine.Pin('LED', machine.Pin.OUT)
ssid = "Mffice_1"
password = "mfficegg"

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

def set_time_from_ntp():
    try:
        ntptime.settime()  # get Time from NTP Server
        print("Time synchronized with NTP")
    except Exception as e:
        print("Failed to synchronize time with NTP:", str(e))


if __name__ == '__main__' :
    if wifi_connect():
        set_time_from_ntp()
    while True:
        rtc_time = time.localtime()
        formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[3], rtc_time[4], rtc_time[5]
        )
        print("Current Time:", formatted_time)
        time.sleep(1) 
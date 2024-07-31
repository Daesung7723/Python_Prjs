print("Scanning for WiFi networks, please wait...")
print("")

import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# for (ssid, bssid, channel, RSSI, authmode, hidden) in sta_if.scan():
for (ssid, bssid, channel, RSSI, authmode, hidden) in sta_if.scan():
  print("* {:s}".format(ssid))  
  print("   - BSSID: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*bssid))
  print("   - Channel: {}".format(channel))
  print("   - RSSI: {}".format(RSSI))
  print()
import telnetlib

HOST = "localhost"
telnet = telnetlib.Telnet(HOST, 5000)

print(telnet.read_all().decode())
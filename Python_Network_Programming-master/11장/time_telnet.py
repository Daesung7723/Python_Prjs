from telnetlib import Telnet
with Telnet('localhost', 5000) as tn:
    msg = tn.read_all()
    print(msg.decode())
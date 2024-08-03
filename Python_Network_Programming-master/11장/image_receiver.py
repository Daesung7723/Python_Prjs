import socket
import pickle

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a specific IP address and port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Accept a connection
print('Waiting for a connection...')
connection, client_address = sock.accept()
print('Connection from', client_address)

# Receive the image data
serialized_data = b''
while True:
    data = connection.recv(4096)
    if not data:
        break
    serialized_data += data

# Deserialize the image data
image_data = pickle.loads(serialized_data)

# Write the image data to a file
with open('d:/received_bookshelf.jpg', 'wb') as f:
    f.write(image_data)

# Close the connection and the socket
print("파일 수신 완료")
connection.close()
sock.close()

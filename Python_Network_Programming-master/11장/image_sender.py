import socket
import pickle

# Open the image file in binary mode
with open('bookshelf.jpg', 'rb') as f:
    image_data = f.read()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's IP address and port
server_address = ('localhost', 10000)
sock.connect(server_address)

# Send the image data using the pickle module
serialized_data = pickle.dumps(image_data)
sock.sendall(serialized_data)
print("파일 전송 완료")
# Close the socket
sock.close()

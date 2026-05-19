#distributed-file-system/server/temp_client.py
import socket

s = socket.socket()

host = 'localhost'
port = 9001

s.connect((host, port))

data = s.recv(1024)

print("Client received:", data.decode())

# send filename
filename = 'to_send'
extension = '.txt'

s.send((filename + extension + '\n').encode())

with open(filename + extension, 'rb') as f:

    while True:

        l = f.read(1024)

        if not l:
            break

        s.send(l)

print('Done sending')

s.close()
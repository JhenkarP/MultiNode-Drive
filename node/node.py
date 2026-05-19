#distributed-file-system/node/node.py
import socket
import sys
import os

s = socket.socket()

host = '0.0.0.0'
print(host)

port = int(sys.argv[1])

s.bind((host, port))

s.listen(5)

print('Node listening on port', port)

while True:

    c, addr = s.accept()

    print('Got connection from', addr)

    c.send(b'Hello Client!')

    header = b''

    while True:

        data = c.recv(1)

        if data == b'\n':
            break

        header += data

    filename = header.decode().strip()

    print("Receiving file:", filename)

    filepath = os.path.join(os.getcwd(), filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as f:

        while True:

            data = c.recv(1024)

            if not data:
                break

            f.write(data)

    print('Successfully received the file')

    c.close()

    print('Connection closed')
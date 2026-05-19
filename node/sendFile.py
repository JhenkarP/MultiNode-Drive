#distributed-file-system/node/sendFile.py
import socket
import sys

s = socket.socket()

host = '0.0.0.0'
print(host)

port = int(sys.argv[1])

s.bind((host, port))

s.listen(5)

print('Server listening on port', port)

while True:

    c, addr = s.accept()

    print('Got connection from', addr)

    c.send(b"Hello Client")

    fileToServe = b''

    while True:

        data = c.recv(1)

        if data == b'\n':
            break

        fileToServe += data

    filename = fileToServe.decode().strip()

    print("Sending file:", filename)

    with open(filename, 'rb') as f:

        while True:

            l = f.read(1024)

            if not l:
                break

            c.send(l)

            print("Sent chunk")

    print('Successfully sent the file')

    c.close()

    print('Connection closed')
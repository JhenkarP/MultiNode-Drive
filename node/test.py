#distributed-file-system/node/test.py
import socket
import os

s = socket.socket()

host = 'localhost'
port = 12345

s.bind((host, port))

s.listen(5)

extension = "mp3"

nodeLocation = r"G:\Test\\" + extension

print("Server listening on port", port)

while True:

    f = open('torecv.png', 'wb')

    c, addr = s.accept()

    print('Got connection from', addr)

    print("Receiving...")

    while True:

        l = c.recv(1024)

        if not l:
            break

        f.write(l)

    f.close()

    print("Done Receiving")

    c.send(b'Thank you for connecting')

    c.close()

print(nodeLocation)

directoryList = {
    "mp3": r"G:\Test\mp3",
    "txt": r"G:\Test\txt",
    "jpeg": r"G:\Test\jpeg"
}

print(directoryList["mp3"])
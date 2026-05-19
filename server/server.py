#distributed-file-system/server/server.py
import socket
import os

s = socket.socket()

host = 'localhost'
port = 12345

s.bind((host, port))

s.listen(5)

print('Server listening...')

while True:

    c, addr = s.accept()

    print('\n[+] Got connection from', addr)

    c.send(b'Hello client!')

    header = b''

    # receive filename
    while True:

        data = c.recv(1)

        if data == b'\n':
            break

        header += data

    header = header.decode().strip()

    # receive file temporarily on server
    with open(header, 'wb') as f:

        print(header, 'opened')

        while True:

            data = c.recv(1024)

            if not data:
                break

            f.write(data)

    print('Successfully received the file', header)

    c.close()

    print('[-] Connection closed with', addr)

    # determine file extension

    host2 = 'localhost'

    filename, file_extension = os.path.splitext(header)

    file_extension = file_extension[1:]

    supported_mappings = ['mp3', 'txt', 'pdf']

    # PRIMARY + BACKUP NODE MAPPING
    extension_port_mapping = {
        'mp3': [9000, 9004],
        'txt': [9001, 9005],
        'pdf': [9002, 9006],
        'others': [9003, 9007]
    }

    if file_extension not in supported_mappings:
        file_extension = 'others'

    ports = extension_port_mapping[file_extension]

    # update index for "updating" state

    to_write = ''

    with open('mIndex/index.txt', 'r') as f:

        for line in f:

            if line.rstrip('\n') == header:
                line = line.rstrip('\n') + '/\n'

            to_write += line

    with open('mIndex/index.txt', 'w') as f:

        f.write(to_write)

    # SEND FILE TO PRIMARY + BACKUP NODES

    for port2 in ports:

        try:

            s2 = socket.socket()

            s2.connect((host2, port2))

            data = s2.recv(1024)

            print('Message received from node:',
                  data.decode())

            # send filename
            s2.send(
                (file_extension + '/' + header + '\n').encode()
            )

            # send actual file
            with open(header, 'rb') as f:

                while True:

                    l = f.read(1024)

                    if not l:
                        break

                    s2.send(l)

            print(
                'Done sending',
                file_extension + '/' + header,
                'to port',
                port2
            )

            s2.close()

        except Exception as e:

            print('Failed to connect to node on port',
                  port2)

            print('Error:', e)

    # remove temporary file from server

    os.remove(header)

    # update index after upload complete

    file_found = False

    to_write = ''

    with open('mIndex/index.txt', 'r') as f:

        for line in f:

            if line.rstrip('\n').rstrip('/') == header:

                line = (
                    line.rstrip('\n')
                    .rstrip('/') + '\n'
                )

                file_found = True

            to_write += line

    if not file_found:

        to_write += header + '\n'

    with open('mIndex/index.txt', 'w') as f:

        f.write(to_write)

    print('\nReplication complete for', header)
#distributed-file-system/server/send_file.py
import socket
import os
import shutil

s = socket.socket()

host = 'localhost'
port = 12346

s.bind((host, port))

s.listen(5)

print('Server listening...')

# CREATE CACHE FOLDER IF NOT EXISTS
os.makedirs("cache", exist_ok=True)

while True:

    c, addr = s.accept()

    print('\n[+] Got connection from', addr)

    c.send(b'Hello client!')

    request = c.recv(1).decode()

    # FETCH FILE LIST
    if request == '1':

        with open("mIndex/index.txt", 'rb') as f:

            c.send(
                b"\nYour files on the server are ('/' means updating):\n"
            )

            while True:

                l = f.read(1024)

                if not l:
                    break

                c.send(l)

    # FETCH SPECIFIC FILE
    elif request == '0':

        header = b''

        while True:

            data = c.recv(1)

            if data == b'\n':
                break

            header += data

        header = header.decode().strip()

        file_exists = 'no'

        with open("mIndex/index.txt", 'r') as f:

            for line in f:

                if line.rstrip('\n') == header:
                    file_exists = 'yes'
                    break

                elif line.rstrip('\n').rstrip('/') == header:
                    file_exists = 'updating'
                    break

        c.send(file_exists.encode())

        if file_exists == 'yes':

            # CHECK CACHE FIRST

            cache_path = os.path.join("cache", header)

            if os.path.exists(cache_path):

                print("Serving file from cache")

                with open(cache_path, 'rb') as f:

                    while True:

                        l = f.read(1024)

                        if not l:
                            break

                        c.send(l)

            else:

                print("File not in cache")

                host2 = 'localhost'

                file_extension = os.path.splitext(header)[1]
                file_extension = file_extension[1:]

                supported_mappings = ['mp3', 'txt', 'pdf']

                if file_extension not in supported_mappings:
                    file_extension = 'others'

                # PRIMARY + BACKUP NODE MAPPING
                extension_port_mapping = {
                    'mp3': [9000, 9004],
                    'txt': [9001, 9005],
                    'pdf': [9002, 9006],
                    'others': [9003, 9007]
                }

                ports = extension_port_mapping[file_extension]

                node_connected = False

                # TRY PRIMARY NODE FIRST
                # IF FAILED -> TRY BACKUP NODE

                for port2 in ports:

                    try:

                        print("Trying node on port", port2)

                        s2 = socket.socket()

                        s2.connect((host2, port2))

                        print("Connected to node server")

                        data = s2.recv(1024)

                        print("Message from node:",
                              data.decode())

                        s2.send(
                            (
                                file_extension +
                                '/' +
                                header +
                                '\n'
                            ).encode()
                        )

                        with open(header, 'wb') as f:

                            print(header,
                                  'opened for writing')

                            while True:

                                data = s2.recv(1024)

                                if not data:
                                    break

                                f.write(data)

                        s2.close()

                        print("Disconnected from node")

                        node_connected = True

                        break

                    except Exception as e:

                        print("Failed to connect to node",
                              port2)

                        print("Error:", e)

                # SEND FILE TO CLIENT

                if node_connected:

                    with open(header, 'rb') as f:

                        while True:

                            l = f.read(1024)

                            if not l:
                                break

                            c.send(l)

                    # SAVE COPY TO CACHE

                    shutil.copy(header, cache_path)

                    print("File added to cache")

                    os.remove(header)

                else:

                    print("All nodes unavailable")

    c.close()

    print('[-] Connection closed with', addr)
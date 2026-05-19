#distributed-file-system/client/fetch.py
import sys
import socket

s = socket.socket()

host = 'localhost'
port = 12346

s.connect((host, port))

data = s.recv(1024)
print("\nMessage from server:", data.decode())

if len(sys.argv) == 1:

    # fetch file list
    s.send("1".encode())

    while True:
        data = s.recv(1024)

        if not data:
            break

        print(data.decode())

else:

    # fetch specific file
    file_to_fetch = sys.argv[1]

    s.send("0".encode())

    s.send((file_to_fetch + '\n').encode())

    exists = s.recv(1024).decode()

    if exists == 'yes':

        with open('target_folder/' + file_to_fetch, 'wb') as f:

            while True:
                data = s.recv(1024)

                if not data:
                    break

                f.write(data)

        print("Successfully received", file_to_fetch,
              "in target_folder/")

    elif exists == 'no':

        print("This file does not exist on the server.")

    else:

        print("This file is currently being updated. Please try again later.")

s.close()
#distributed-file-system/client/client_watch.py
import time
import socket
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):

    def send_to_server(self, event):

        filename = os.path.split(event.src_path)[1]

        s = socket.socket()
        host = 'localhost'
        port = 12345

        s.connect((host, port))

        data = s.recv(1024)
        print("Client received:", data.decode())

        s.send((filename + '\n').encode())

        with open(event.src_path, 'rb') as f:
            while True:
                l = f.read(1024)
                if not l:
                    break
                s.send(l)

        print("Done sending", filename)
        s.close()

    def on_modified(self, event):

        if event.is_directory:
            return

        self.send_to_server(event)

event_handler = MyHandler()

observer = Observer()
observer.schedule(event_handler, './source_folder/', recursive=False)

observer.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()
import socket
import threading
from queue import Queue
import sys


class Client:
    def __init__(self, workers, path):
        self.path = path
        self.adress = ("localhost", 777)

        self.workers = workers
        self.send_client_workers()

        self.lock = threading.Lock()
        self.counter = 0

    def send_client_workers(self):
        tcp_socket = socket.socket()
        tcp_socket.connect(self.adress)
        tcp_socket.send(f"{self.workers}".encode(encoding="utf_8"))
        tcp_socket.close()

    def disconnect_from_server(self):
        tcp_socket = socket.socket()
        tcp_socket.connect(self.adress)
        tcp_socket.send("!disconnect".encode(encoding="utf_8"))
        tcp_socket.close()

    def send_and_recieve(self, que):
        while True:
            try:
                url = que.get()
                if url is None:
                    break
            except Exception:
                continue

            tcp_socket = socket.socket()
            tcp_socket.connect(self.adress)

            tcp_socket.send(url.encode(encoding="utf_8"))
            data = tcp_socket.recv(1024).decode(encoding="utf_8")

            with self.lock:
                print(f"{url}: {data}")
                self.counter += 1
            tcp_socket.close()

    def work(self):
        file = open(self.path, "r", encoding="utf-8")
        que = Queue()

        threads = [
            threading.Thread(target=self.send_and_recieve, args=(que,))
            for _ in range(self.workers)
        ]

        for thread in threads:
            thread.start()

        for url in file.readlines():
            que.put(url.strip())

        for _ in range(len(threads)):
            que.put(None)

        for thread in threads:
            thread.join()

        self.disconnect_from_server()
        file.close()


if __name__ == "__main__":
    m, root = int(sys.argv[1]), sys.argv[2]
    client = Client(m, root)
    client.work()

import socket
import threading
import queue


class Client:
    def __init__(self, workers, path):
        self.workers = workers
        self.path = path
        self.adress = ("localhost", 777)
        self.lock = threading.Lock()
        self.send_num_workers()

    def send_num_workers(self):
        tcp_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # socket.AF_UNIX for UNIX systems
        tcp_socket.connect(self.adress)
        tcp_socket.send(f"{self.workers}".encode(encoding="utf_8"))
        tcp_socket.close()

    def send_and_recieve(self, que):
        while True:
            tcp_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )  # socket.AF_UNIX for UNIX systems
            tcp_socket.connect(self.adress)

            try:
                url = que.get()
            except Exception:
                continue

            if url is None:
                with self.lock:
                    tcp_socket.send("!disconnection".encode(encoding="utf_8"))
                tcp_socket.close()
                break

            with self.lock:
                tcp_socket.send(url.encode(encoding="utf_8"))

            data = tcp_socket.recv(1024).decode(encoding="utf_8")
            with self.lock:
                print(f"{url}: {data}")
                tcp_socket.close()

    def work(self):
        file = open(self.path, "r", encoding="utf-8")
        que = queue.Queue(20)

        threads = [
            threading.Thread(
                target=self.send_and_recieve,
                args=(que,),
            )
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

        tcp_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # socket.AF_UNIX for UNIX systems
        tcp_socket.connect(self.adress)
        tcp_socket.send("!None".encode(encoding="utf_8"))
        tcp_socket.close()


if __name__ == "__main__":
    path = r"D:\projects\deep_python_autumn_2022\06\URLS.txt"
    workers = 1

    client = Client(workers, path)
    client.work()

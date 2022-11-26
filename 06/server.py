import threading
from queue import Queue
from urllib.request import urlopen
import socket
import re
from collections import Counter
import sys
from json import dumps
from bs4 import BeautifulSoup

from utils import delete_uninteresting_words


class Server:
    def __init__(self, workers, k):
        self.k = k
        self.server = None
        self.workers = workers
        self.break_loop = False

        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("localhost", 777))
        self.server.settimeout(1)

        self.lock = threading.Lock()
        self.counter = 0

    def parse_html(self, raw_data):
        soup = BeautifulSoup(raw_data, "html.parser")
        data = re.split(r"[\d\W+]", soup.get_text(strip=False))

        counter = Counter([word.lower() for word in data])
        counter = delete_uninteresting_words(counter)
        return dumps(dict(counter.most_common(self.k)), ensure_ascii=False)

    def fetch_url(self, url):
        try:
            with urlopen(url) as resp:
                data = self.parse_html(resp.read().decode("utf-8"))
                return data

        except Exception:
            with self.lock:
                print(f"URL {url} does not exist")
            return None

    def fetch_and_send(self, que):
        while not self.break_loop:
            try:
                client_socket = que.get(timeout=0.1)
                url = client_socket.recv(1024).decode(encoding="utf_8")

                if url == "!disconnect":
                    self.break_loop = True
                    continue

                data = self.fetch_url(url)

                if data is None:
                    data = "URL does not exist"
                    client_socket.send(data.encode())
                else:
                    client_socket.send(data.encode())
                    with self.lock:
                        self.counter += 1
                        print(f"URL downloaded: {self.counter}")
                client_socket.close()

            except Exception:
                continue

    def work(self):
        que = Queue()
        self.server.listen()

        threads = [
            threading.Thread(
                target=self.fetch_and_send,
                args=(que,),
            )
            for _ in range(self.workers)
        ]

        for thread in threads:
            thread.start()

        while not self.break_loop:
            try:
                client_socket, _ = self.server.accept()
                que.put(client_socket)

            except Exception:
                continue

        for thread in threads:
            thread.join()

        self.server.close()


if __name__ == "__main__":
    w, m = int(sys.argv[2]), int(sys.argv[4])
    server = Server(w, m)
    server.work()

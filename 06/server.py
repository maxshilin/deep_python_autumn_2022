import threading
import queue
from urllib.request import urlopen
from urllib.error import HTTPError
import socket
import re
from collections import Counter

# import sys
from json import dumps
from bs4 import BeautifulSoup


class Server:
    def __init__(self, workers, k):
        self.workers = workers
        self.k = k

        self.server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # socket.AF_UNIX for UNIX systems
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("localhost", 777))
        self.server.listen()
        self.client_socket, _ = self.server.accept()

        self.lock = threading.Lock()
        self.counter = 0

    def fetch_url(self, url):
        try:
            resp = urlopen(url)

        except HTTPError:
            with self.lock:
                print(f"URL {url.strip()} does not exist")
            return None

        raw_data = resp.read().decode("utf-8")
        resp.close()
        soup = BeautifulSoup(raw_data, "html.parser")
        data = re.split(r"[\d\W+]", soup.get_text(strip=False))

        counter = Counter([word.lower() for word in data if word != ""])
        return dumps(dict(counter.most_common(self.k)), ensure_ascii=False)

    def fetch_and_send(self, que):
        while True:
            try:
                url = que.get(timeout=1)
                if url is None:
                    break

            except Exception:
                continue

            data = self.fetch_url(url)

            with self.lock:
                if data is None:
                    data = "URL does not exist"
                    self.client_socket.send(data.encode())
                else:
                    self.client_socket.send(data.encode())
                    self.counter += 1
                    print(f"URL downloaded: {self.counter}")

    def work(self):
        que = queue.Queue(20)

        threads = [
            threading.Thread(
                target=self.fetch_and_send,
                args=(que,),
            )
            for _ in range(self.workers)
        ]

        for thread in threads:
            thread.start()

        while True:
            url = self.client_socket.recv(1024).decode(encoding="utf_8")
            if len(url) == 0:
                break

            que.put(url)

        for _ in range(self.workers):
            que.put(None)

        for thread in threads:
            thread.join()

        self.server.close()


if __name__ == "__main__":
    # w, k = sys.argv[2], sys.argv[4]
    server = Server(10, 5)
    server.work()

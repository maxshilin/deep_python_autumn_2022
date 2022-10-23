import threading
from queue import Queue
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
        self.k = k

        self.server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # socket.AF_UNIX for UNIX systems
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("localhost", 777))

        self.client_workers = self.recieve_clients_workers()
        self.workers = workers

        self.lock = threading.Lock()
        self.counter = 0

    def recieve_clients_workers(self):
        self.server.listen()
        client_socket, _ = self.server.accept()
        num = client_socket.recv(1024).decode(encoding="utf_8")
        client_socket.close()
        return int(num)

    def parse_html(self, raw_data):
        ignore = [
            "",
            "the",
            "a",
            "if",
            "in",
            "it",
            "of",
            "or",
            "and",
            "is",
            "to",
            "by",
            "on",
            "that",
            "from",
            "s",
            "t",
            "mathbf",
        ]
        soup = BeautifulSoup(raw_data, "html.parser")
        data = re.split(r"[\d\W+]", soup.get_text(strip=False))

        counter = Counter([word.lower() for word in data])
        for word in ignore:
            if word in counter:
                del counter[word]
        return dumps(dict(counter.most_common(self.k)), ensure_ascii=False)

    def fetch_url(self, url):
        try:
            resp = urlopen(url)

        except HTTPError:
            with self.lock:
                print(f"URL {url} does not exist")
            return None

        data = self.parse_html(resp.read().decode("utf-8"))
        resp.close()
        return data

    def fetch_and_send(self, que, connections):
        while True:
            try:
                url = que.get(timeout=1)
                client_socket = connections.get(timeout=1)
                if url == "!disconnection":
                    client_socket.close()
                    break

            except Exception:
                continue

            data = self.fetch_url(url)

            with self.lock:
                if data is None:
                    data = "URL does not exist"
                    client_socket.send(data.encode())
                else:
                    client_socket.send(data.encode())
                    self.counter += 1
                    print(f"URL downloaded: {self.counter}")
                client_socket.close()

    def work(self):
        que = Queue(2 * self.client_workers)
        connections = Queue(2 * self.client_workers)

        threads = [
            threading.Thread(
                target=self.fetch_and_send,
                args=(que, connections),
            )
            for _ in range(self.workers)
        ]

        for thread in threads:
            thread.start()

        while True:
            self.server.listen(2 * self.client_workers)
            client_socket, _ = self.server.accept()
            url = client_socket.recv(1024).decode(encoding="utf_8")
            print(url)
            if url == "!None":
                break

            que.put(url)
            connections.put(client_socket)

        for thread in threads:
            thread.join()

        self.server.close()


if __name__ == "__main__":
    # w, k = sys.argv[2], sys.argv[4]
    server = Server(10, 5)
    server.work()

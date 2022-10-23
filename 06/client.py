import socket
import threading
import queue


def send_and_recieve(que, tcp_socket, lock):
    while True:
        try:
            url = que.get()
            if url is None:
                break

        except Exception:
            continue

        with lock:
            tcp_socket.send(url.encode(encoding="utf_8"))

        data = tcp_socket.recv(1024).decode(encoding="utf_8")
        with lock:
            print(f"{url.strip()}: {data}")


addr = ("localhost", 777)
path = r"D:\projects\deep_python_autumn_2022\06\URLS.txt"
file = open(path, "r", encoding="utf-8")

tcp_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # socket.AF_UNIX for UNIX systems

tcp_socket.connect(addr)

que = queue.Queue(20)

lock = threading.Lock()

threads = [
    threading.Thread(
        target=send_and_recieve,
        args=(que, tcp_socket, lock),
    )
    for _ in range(10)
]

for thread in threads:
    thread.start()

for url in file.readlines():
    que.put(url)

for i in range(len(threads)):
    que.put(None)

for thread in threads:
    thread.join()

tcp_socket.close()

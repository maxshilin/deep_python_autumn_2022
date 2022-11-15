import asyncio
import threading
from queue import Empty
from queue import Queue
import sys
import re
from collections import Counter
from bs4 import BeautifulSoup
import aiohttp

from utils import delete_uninteresting_words


def parse_html(url_que, data_que):
    while True:
        try:
            url = url_que.get(timeout=0.1)
            if url is None:
                url_que.task_done()
                break

            raw_data = data_que.get(timeout=0.1)
            soup = BeautifulSoup(raw_data, "html.parser")
            data = re.split(r"[\d\W+]", soup.get_text(strip=False))

            counter = Counter([word.lower() for word in data])
            counter = delete_uninteresting_words(counter)
            print(f"Url {url.strip()}: {dict(counter.most_common(5))}")

        except Empty:
            continue


async def fetch(session, que, url_que, data_que):
    while True:
        url = await que.get()

        try:
            async with session.get(url) as resp:
                raw_data = await resp.read()
                assert resp.status == 200
                url_que.put(url)
                data_que.put(raw_data)
        finally:
            que.task_done()


async def batch_fetch(urls, workers):
    que = asyncio.Queue()
    url_que = Queue()
    data_que = Queue()

    thread = threading.Thread(
        target=parse_html,
        args=(url_que, data_que),
    )

    thread.start()

    with open(urls, "r", encoding="utf_8") as file:
        for url in file.readlines():
            await que.put(url)

    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(fetch(session, que, url_que, data_que))
            for _ in range(workers)
        ]
        await que.join()

        url_que.put(None)
        thread.join()

        for worker in workers:
            worker.cancel()


if __name__ == "__main__":
    num, root = int(sys.argv[1]), sys.argv[2]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(batch_fetch(root, num))

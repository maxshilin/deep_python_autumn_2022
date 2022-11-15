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


class Async_URLS:
    def __init__(self, urls, workers):
        self.urls = urls
        self.workers = workers

        self.counter = 0
        self.parse_counter = 0

    @staticmethod
    def parse_html(raw_data):
        soup = BeautifulSoup(raw_data, "html.parser")
        data = re.split(r"[\d\W+]", soup.get_text(strip=False))

        counter = Counter([word.lower() for word in data])
        counter = delete_uninteresting_words(counter)
        return dict(counter.most_common(5))

    def thread_worker(self, url_que, data_que):
        while True:
            try:
                url = url_que.get(timeout=0.1)
                if url is None:
                    url_que.task_done()
                    break

                raw_data = data_que.get(timeout=0.1)
                out = self.parse_html(raw_data)
                self.parse_counter += 1
                print(f"Url {url.strip()}: {out}")

            except Empty:
                continue

    async def fetch(self, session, que, url_que, data_que):
        while True:
            url = await que.get()

            try:
                async with session.get(url) as resp:
                    raw_data = await resp.read()
                    assert resp.status == 200
                    url_que.put(url)
                    data_que.put(raw_data)
                    self.counter += 1
            finally:
                que.task_done()

    async def batch_fetch(self):
        que = asyncio.Queue()
        url_que = Queue()
        data_que = Queue()

        thread = threading.Thread(
            target=self.thread_worker,
            args=(url_que, data_que),
        )

        thread.start()

        with open(self.urls, "r", encoding="utf_8") as file:
            for url in file.readlines():
                await que.put(url)

        async with aiohttp.ClientSession() as session:
            workers = [
                asyncio.create_task(
                    self.fetch(session, que, url_que, data_que)
                )
                for _ in range(self.workers)
            ]
            await que.join()

            url_que.put(None)
            thread.join()

            for worker in workers:
                worker.cancel()


if __name__ == "__main__":
    num, root = int(sys.argv[1]), sys.argv[2]

    loop = asyncio.get_event_loop()
    crawler = Async_URLS(root, num)
    loop.run_until_complete(crawler.batch_fetch())

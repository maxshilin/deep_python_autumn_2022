import asyncio
from unittest import mock
from io import StringIO
from queue import Queue
import aiohttp
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web

from fetcher import Async_URLS


class TestServer(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        return app

    async def test_successful(self):
        crawler = Async_URLS("urls.txt", 1)
        url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

        que = asyncio.Queue()
        data_que = Queue()

        await que.put(url)

        async with aiohttp.ClientSession() as session:
            task = asyncio.create_task(crawler.fetch(session, que, data_que))
            await que.join()
            task.cancel()

        downloaded_url, _ = data_que.get()
        self.assertEqual(crawler.counter, 1)
        self.assertEqual(crawler.parse_counter, 0)
        self.assertEqual(url, downloaded_url)

    async def test_unsuccessful(self):
        crawler = Async_URLS("urls.txt", 1)
        url = "https://en.wikipedia/Python_(programming_language)"

        que = asyncio.Queue()
        data_que = Queue()

        await que.put(url)

        with mock.patch(
            "fetcher.sys.stdout", new_callable=StringIO
        ) as print_mock:
            async with aiohttp.ClientSession() as session:
                asyncio.create_task(crawler.fetch(session, que, data_que))
                await que.join()
                print_server = print_mock.getvalue()

        self.assertEqual(crawler.counter, 0)
        self.assertEqual(crawler.parse_counter, 0)
        self.assertEqual(f"Url {url}: does not exist\n", print_server)

    @mock.patch("fetcher.Async_URLS.parse_html")
    def test_download(self, parser_mock):
        parser_mock.return_value = ""
        crawler = Async_URLS("urls.txt", 10)

        with mock.patch(
            "fetcher.sys.stdout", new_callable=StringIO
        ) as print_mock:
            asyncio.run(crawler.batch_fetch())
            print_server = map(
                lambda x: x.split(" ")[1][:-1],
                print_mock.getvalue().split("\n")[:-1],
            )

        with open("urls.txt", "r", encoding="utf_8") as file:
            data = file.readlines()
            urls = [x.strip() for x in data]

        self.assertEqual(crawler.counter, 100)
        self.assertEqual(crawler.parse_counter, 100)
        self.assertListEqual(sorted(urls), sorted(print_server))


if __name__ == "__main__":
    AioHTTPTestCase.main()

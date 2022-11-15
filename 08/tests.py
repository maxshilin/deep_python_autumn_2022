import asynctest
import asyncio
from unittest import mock
from io import StringIO

from fetcher import Async_URLS


class testServer(asynctest.TestCase):
    @mock.patch("fetcher.Async_URLS.parse_html")
    def test_that_a_coroutine_runs(self, parser_mock):
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

        file = open("urls.txt", "r", encoding="utf_8")
        data = file.readlines()
        urls = [x.strip() for x in data]
        file.close()

        self.assertEqual(crawler.counter, 100)
        self.assertEqual(crawler.parse_counter, 100)
        self.assertListEqual(sorted(urls), sorted(print_server))


if __name__ == "__main__":
    asynctest.main()

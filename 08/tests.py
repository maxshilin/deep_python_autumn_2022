import asyncio
import asynctest
from unittest import mock

from fetcher import batch_fetch


class testServer(asynctest.TestCase):
    @mock.patch("fetcher.parse_html")
    def test_that_a_coroutine_runs(self, _):
        result = self.loop.run_until_complete(batch_fetch("urls.txt", 10))
        print(result)

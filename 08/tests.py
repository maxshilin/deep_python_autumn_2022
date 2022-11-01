import asyncio
import asynctest

from fetcher import batch_fetch


class testServer(asynctest.TestCase):
    async def a_coroutine(self):
        return "I worked"

    def setUp(self):
        self.my_loop = asyncio.new_event_loop()

    def test_that_a_coroutine_runs(self):
        result = self.my_loop.run_until_complete(self.a_coroutine())
        self.assertIn("worked", result)

    def tearDown(self):
        self.my_loop.close()

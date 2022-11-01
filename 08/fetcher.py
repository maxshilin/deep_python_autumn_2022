import asyncio
import sys

import aiohttp


async def fetch(session, que):
    while True:
        url = await que.get()

        try:
            async with session.get(url) as resp:
                await resp.read()
                assert resp.status == 200
        finally:
            que.task_done()

        print(f"Url {url.strip()} has successfully downloaded")


async def batch_fetch(urls, workers):
    que = asyncio.Queue()

    with open(urls, "r", encoding="utf_8") as file:
        for url in file.readlines():
            await que.put(url)

    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(fetch(session, que)) for _ in range(workers)
        ]
        await que.join()

        for worker in workers:
            worker.cancel()


if __name__ == "__main__":
    num, root = int(sys.argv[1]), sys.argv[2]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(batch_fetch(root, num))

import argparse
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from collections import Counter


class Client:
    def __init__(self, host, port, task_count, urls_file, top_k=5, debug=False):
        if task_count <= 0:
            raise ValueError("Tasks count must be > 0")

        self.host = host
        self.port = port
        self.task_count = task_count
        self.urls_file = urls_file
        self.top_k = top_k
        self.debug = debug
        self.que = asyncio.Queue()
        if self.debug:
            self.tasks_created = 0
            self.processed_urls = 0

    def __str__(self):
        return f"Client {self.urls_file=}; {self.task_count=}; {self.top_k=}"

    def start(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.run_tasks())
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    async def run_tasks(self):
        async with aiohttp.ClientSession() as session:
            # Создание асинхронных задач
            workers = [self.create_tasks()]
            workers.extend([self.worker(session) for _ in range(self.task_count)])

            if self.debug:
                self.tasks_created = len(workers)
                print(f"\033[33mTasks created: {self.tasks_created}\033[0m")

            await asyncio.gather(*workers)

    async def create_tasks(self):
        for url in self.get_url():
            await self.que.put(url)
        await self.que.put(None)

    def get_url(self):
        with open(self.urls_file, "r") as file:
            for url in file:
                yield url.strip()

    async def worker(self, session):
        while True:
            url = await self.que.get()
            if url is None:
                await self.que.put(None)
                break

            try:
                response = await self.fetch_url(session, url)
            except aiohttp.client_exceptions.ClientConnectorError as e:
                print(f"\033[91mError connecting to {url}: {e}\033[0m")
                continue
            except Exception as e:
                print(f"\033[91mFailed to retrieve the URL '{url}': {e}[0m]")
                continue

            # Эту нагрузку на CPU лучше вынести в отдельный поток
            result = self.parse_html(response)
            result = f"URL: {url[:20]}...'\Top {self.top_k} words: {result}"
            print(result)

            if self.debug:
                self.processed_urls += 1
                print(f"\033[33mTotally urls processed: {self.processed_urls}\033[0m")

    async def fetch_url(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    def parse_html(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text()
        top_words = self.get_top_words(text)
        return top_words

    def get_top_words(self, text):
        words = text.split()
        word_count = Counter(words)
        top_words = word_count.most_common(self.top_k)
        top_words_dict = {word: count for word, count in top_words}
        return top_words_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for Master-Worker Server")
    parser.add_argument("urls_file", help="File containing URLs")
    parser.add_argument(
        "-c", "--task_count", default=5, type=int, help="Count of asynchronous requests"
    )
    parser.add_argument(
        "-k", "--top_k", type=int, default=5, help="Top K words to return"
    )
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    client = Client(
        args.host,
        args.port,
        args.task_count,
        args.urls_file,
        top_k=args.top_k,
        debug=args.debug,
    )
    client.start()

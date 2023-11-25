import argparse
import json
import socket
import threading
from collections import Counter
from queue import Queue

import requests
from bs4 import BeautifulSoup


class Server:
    def __init__(self, host, port, num_workers, top_k, debug=False):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k
        self.url_queue = Queue()  # Очередь для URL-ов, которые нужно обработать
        self.processed_urls = 0  # Счетчик обработанных URL-ов
        self.workers = []  # Список воркеров
        self.debug = debug
        self.lock = threading.Lock()

    def start(self):
        if self.debug:
            print("Starting workers...")

        self.create_workers()

        if self.debug:
            print("Starting listening...")

        self.start_listening()

    def create_workers(self):
        for _ in range(self.num_workers):
            worker = Worker(self)
            self.workers.append(worker)
            worker.start()

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server is listening on {self.host}:{self.port}")

            while True:
                # По хорошему закрывать соединение там, где его создал, но я
                # не придумал как мне так сделать, учитывая мои потоки
                client_socket, client_address = server_socket.accept()

                self.url_queue.put(client_socket)
                if self.debug:
                    print(f"\033[33mQueue len {self.url_queue.qsize()}\033[0m")


class Worker(threading.Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.name = f"Worker {self.name}"

    def run(self):
        while True:
            if self.server.debug:
                print(f"{self.name} ready to accept")

            client_socket = self.server.url_queue.get()

            if self.server.debug:
                print(f"{self.name} accepted")

            try:
                data = client_socket.recv(1024)
                url = data.decode("utf-8")

                result = self.process_url(url)

                client_socket.send(result.encode("utf-8"))
            except Exception as e:
                print(f"Error: {str(e)}")
            finally:
                client_socket.close()

    def process_url(self, url):
        if self.server.debug:
            print(f"{self.name} processing url '{url}'...")

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                text = self.parse_html(response.text)
                top_words = self.get_top_words(text)
                result = (
                    f"Top {self.server.top_k} words in '{url[:20]}...': {top_words}"
                )
                if self.server.debug:
                    print(result)
            else:
                result = json.dumps({"error": f"Failed to retrieve the URL: {url}"})
                print(f"\033[91m{result}\033[0m")

        except Exception as e:
            result = json.dumps({"error": str(e)})
            print(f"\033[91m{result}[0m]")

        with self.server.lock:
            self.server.processed_urls += 1
            print(
                f"\033[33mTotally urls processed: {self.server.processed_urls}\033[0m"
            )

        return result

    def parse_html(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text()
        return text

    def get_top_words(self, text):
        words = text.split()
        word_count = Counter(words)
        top_words = word_count.most_common(self.server.top_k)
        top_words_dict = {word: count for word, count in top_words}
        return top_words_dict


# Запуск сервера
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master-Worker Server")
    parser.add_argument(
        "-w", "--num_workers", type=int, default=3, help="Number of workers"
    )
    parser.add_argument(
        "-k", "--top_k", type=int, default=7, help="Top K words to return"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to listen on")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    server = Server(
        args.host, args.port, args.num_workers, args.top_k, debug=args.debug
    )
    server.start()

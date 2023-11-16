import argparse
import socket
import threading
from queue import Queue


class Client:
    def __init__(self, host, port, num_threads, urls_file, debug=False):
        if num_threads <= 0:
            raise ValueError("Threads count must be > 0")

        self.host = host
        self.port = port
        self.num_threads = num_threads
        self.urls_file = urls_file
        self.debug = debug
        self.url_queue = Queue()

    def get_url(self):
        with open(self.urls_file, "r") as file:
            for url in file:
                yield url.strip()

    def start(self):
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.send_requests)
            threads.append(thread)
            thread.start()

        for url in self.get_url():
            self.url_queue.put(url)
        self.url_queue.put(None)

        for thread in threads:
            thread.join()

    def send_requests(self):
        while True:
            if self.debug:
                print(f"{threading.current_thread().name} ready to accept")

            url = self.url_queue.get()

            if url is None:
                self.url_queue.put(None)
                if self.debug:
                    print(f"===== {threading.current_thread().name} stopped =====")
                break

            try:
                if self.debug:
                    print(f"{threading.current_thread().name} accepted url {url[:20]}")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.host, self.port))
                    client_socket.send(url.encode("utf-8"))
                    response = client_socket.recv(1024).decode("utf-8")
                    print(response)

            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for Master-Worker Server")
    parser.add_argument("num_threads", type=int, help="Number of threads")
    parser.add_argument("urls_file", help="File containing URLs")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    client = Client(
        args.host, args.port, args.num_threads, args.urls_file, debug=args.debug
    )
    client.start()

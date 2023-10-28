import argparse
import socket
import threading


class Client:
    def __init__(self, host, port, num_threads, urls_file, debug=False):
        self.host = host
        self.port = port
        self.num_threads = num_threads
        self.urls_file = urls_file
        self.debug = debug

    def start(self):
        with open(self.urls_file, "r") as file:
            urls = file.readlines()

        threads = []
        # Для первых
        remains = len(urls) % self.num_threads
        size = len(urls) // self.num_threads
        start = 0
        end = 0

        for i in range(self.num_threads):
            end += size
            if i < remains:
                end += 1

            thread = threading.Thread(
                target=self.send_requests, args=(urls[start:end],)
            )
            threads.append(thread)
            thread.start()
            start = end

        for thread in threads:
            thread.join()

    def send_requests(self, urls):
        try:
            if self.debug:
                print(threading.current_thread().name, len(urls))
            while urls:
                url = urls.pop()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.host, self.port))
                    client_socket.send(url.encode("utf-8").strip())
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

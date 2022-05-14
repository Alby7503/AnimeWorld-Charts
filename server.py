"""Animeworld.tv chart server"""
from logging import INFO, basicConfig, info
from socket import socket

from requests import get


class Server:
    """HTTP Server"""

    def __init__(self, host, port):
        basicConfig(filename="server.log", level=INFO)
        self.host = host
        self.port = port
        self.sock = socket()
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

    def run(self):
        """Serve HTML"""
        while True:
            try:
                client, addr = self.sock.accept()
                info(f"Client connected: {addr}")
                client.settimeout(1)
                data = client.recv(1024).decode().splitlines()
                data[0] = data[0].split(' ')
                method = data[0][0]
                if method == "GET":
                    path = data[0][1]
                    if path == '/':
                        with open("index.html", 'r', encoding="ascii") as file:
                            client.send(file.read().encode())
                    elif path.startswith("/search/"):
                        code = path.rsplit('/', maxsplit=1)[1]
                        client.send(
                            get("https://www.animeworld.tv/watchlist/" + code).text.encode())
                    else:
                        client.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                else:
                    client.send(b'HTTP/1.1 405 Method Not Allowed\r\n\r\n')
                print(data)
            except Exception:
                continue


Server("127.0.0.1", 80).run()

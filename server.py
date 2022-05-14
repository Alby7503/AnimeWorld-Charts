"""Animeworld.tv chart server"""
from logging import INFO, basicConfig, info
from socket import socket
from os import environ

from requests import get

HEADERS = {
    "server": "Socket Server",
    "date": "Tue, 15 Nov 1994 08:12:31 GMT",
    "content-type": "text/html; charset=ascii"
}


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
                            self.http_response(
                                client, 200, "OK", [], file.read())
                    elif path.startswith("/search/"):
                        code = path.rsplit('/', maxsplit=1)[1]
                        self.http_response(client, 200, "OK", [], get(
                            "https://www.animeworld.tv/watchlist/" + code).text)
                    else:
                        self.http_response(client, 404, "Not Found", [])
                else:
                    self.http_response(
                        client, 405, "Method Not Allowed", [])
                print(data)
            except Exception:
                continue

    def http_response(self, client, code, message, headers, body=''):
        """HTTP response"""
        headers["content-length"] = len(body)
        response = f"HTTP/1.1 {code} {message}\r\n"
        for header in headers:
            response += f"{header[0]}: {header[1]}\r\n"
        response += "\r\n"
        response += body
        client.send(response.encode())


#nviron["PORT"] = "80"
Server("0.0.0.0", int(environ["PORT"])).run()

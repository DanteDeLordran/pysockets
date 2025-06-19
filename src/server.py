import socket
import threading


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: list[socket.socket] = []
        self.nicknames: list[str] = []

    def broadcast(self, message: bytes) -> None:
        for client in self.clients:
            client.send(message)

    def handle(self, client: socket.socket) -> None:
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except Exception as e:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)

                self.broadcast(f"{nickname} had error {e}".encode("ascii"))
                self.broadcast(f"{nickname} left the chat".encode("ascii"))

                break

    def recieve(self) -> None:
        while True:
            client, address = self.server.accept()
            print(f"Connected with {address}")

            client.send("NICK".encode("ascii"))
            nickname = client.recv(1024).decode("ascii")
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"Nickname of the client is : {nickname}")
            self.broadcast(f"{nickname} joined the chat".encode("ascii"))
            client.send("Connected to the server".encode("ascii"))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server is listening on port: {self.port}")
        self.recieve()

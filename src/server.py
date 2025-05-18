import socket
from datetime import datetime
from db import db
from message import Message
import threading


class Server:
    def __init__(
        self, ip: str = "127.0.0.1", port: int = 8000, max_connections: int = 5
    ) -> None:
        self.ip = ip
        self.port = port
        self.max_connections = max_connections
        self.running = False
        self.server_socket = None
        self.connections: list[socket.socket] = []

    async def handle_client(self, client_socket: socket.socket, client_addres: tuple):
        print(f"Accepted connection from {client_addres[0]} {client_addres[1]}")

        while self.running:
            try:
                request = client_socket.recv(1024).decode("utf-8")
                if not request:
                    print("No request recieved")
                    break
                if request.lower() == "close":
                    client_socket.send("closed".encode("utf-8"))
                    break

                print(f"Recieved from {client_addres}: {request}")

                message = Message(
                    timestamp=datetime.now(),
                    source_port=self.port,
                    client_address=f"{client_addres[0]}:{client_addres[1]}",
                    message=request,
                )

                await db.new_message(message)

                self.broadcast(request, exclude=client_socket)

                response = "Message recieved and stored".encode("utf-8")
                client_socket.send(response)

            except Exception as e:
                print(f"Error with client {client_addres} fue to {e}")
                break

        client_socket.close()
        if client_socket in self.connections:
            self.connections.remove(client_socket)
        print(f"Connection closed with {client_addres}")

    def broadcast(self, message: str, exclude: socket.socket | None = None):
        for connection in self.connections:
            if connection != exclude:
                try:
                    connection.send(message.encode("utf-8"))
                except Exception as e:
                    print(f"Broadcast error: {e}")

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(self.max_connections)
        self.running = True
        print(f"Server listening on {self.ip} {self.port}")

        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                self.connections.append(client_socket)
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True,
                )
                client_thread.start()
        except Exception as e:
            raise Exception(f"Server error due to {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        for connection in self.connections:
            connection.close()
        if self.server_socket:
            self.server_socket.close()
        print(f"Server on port {self.port} stopped")

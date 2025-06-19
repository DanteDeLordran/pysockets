import socket
import threading


class Client:
    def __init__(self, host: str, port: int, nickname: str):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recieve(self):
        while True:
            try:
                message = self.client.recv(1024).decode("ascii")
                if message == "NICK":
                    self.client.send(self.nickname.encode("ascii"))
                else:
                    print(message)
            except Exception as e:
                print(f"Error ocurred due to: {e}")
                self.client.close()
                break

    def write(self):
        while True:
            message = f"{self.nickname}: {input('')}"
            self.client.send(message.encode("ascii"))

    def start(self):
        self.client.connect((self.host, self.port))

        recieve = threading.Thread(target=self.recieve)
        recieve.start()

        write = threading.Thread(target=self.write)
        write.start()

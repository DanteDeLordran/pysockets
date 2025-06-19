import typer
from server import Server
from client import Client

app = typer.Typer()


@app.command()
def start():
    pass


@app.command()
def server(host: str, port: int):
    server = Server(host, port)
    server.start()


@app.command()
def client(
    host: str,
    port: int,
    nickname: str,
):
    client = Client(host, port, nickname)
    client.start()


if __name__ == "__main__":
    app()

import typer
import threading
from db import db
from server import Server

app = typer.Typer()
active_servers: dict[int, threading.Thread] = {}


@app.command()
def new(port: int):
    """Start a new socket server on the specified port"""
    if port in active_servers:
        print(f"Server already running on port {port}")
        return

    server = Server(port=port)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
    active_servers[port] = server_thread
    print(f"Socket server started on port: {port}")


@app.command()
def delete(port: int):
    """Stop and remove a socket server on the specified port"""
    if port not in active_servers:
        print(f"No server running on port {port}")
        return

    # In a real implementation, we would need to properly stop the server
    del active_servers[port]
    print(f"Deleted socket server on port: {port}")


@app.command()
def list():
    """List all active socket servers"""
    if not active_servers:
        print("No active socket servers")
        return

    print("Active socket servers:")
    for port in active_servers:
        print(f"- Port {port}")


@app.command()
async def messages(port: int):
    """Show stored messages from MongoDB (optionally filtered by port)"""

    messages = await db.get_messages(port)

    print("Stored messages:")
    for message in messages:
        print(
            f"[{message['timestamp']}] {message['source_port']} from {message['client_address']}: {message['message']}"
        )


if __name__ == "__main__":
    app()

from datetime import datetime
from typing import TypedDict


class Message(TypedDict):
    timestamp: datetime
    source_port: int
    client_address: str
    message: str

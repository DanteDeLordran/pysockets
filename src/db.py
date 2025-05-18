from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from message import Message


class Database:
    def __init__(
        self, uri: str = "mongodb://root:root@localhost:27017", name: str = "socket_db"
    ) -> None:
        self.client = AsyncMongoClient(uri)
        self.db = self.client[name]
        self.messages: AsyncCollection[Message] = self.db["messages"]

    async def new_message(self, message: Message) -> str | None:
        try:
            result = self.messages.insert_one(message)
            return str(result)
        except Exception as e:
            print(f"Error inserting message due to: {e}")
            return None

    async def get_messages(self, port: int) -> list[Message]:
        messages = self.messages.find({"source_port": port}).sort("timestamp")
        return await messages.to_list()


db = Database()

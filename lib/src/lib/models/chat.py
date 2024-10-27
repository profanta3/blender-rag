from typing import Literal
from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "system", "bot"]
    content: str


# class UserMessage(Message):
#     role: str = "user"


# class BotMessage(Message):
#     role: str = "bot"


# class SystemMessage(Message):
#     role: str = "system"

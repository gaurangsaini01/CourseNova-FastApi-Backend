from pydantic import BaseModel
from typing import Optional


class ChatBotSchema(BaseModel):
    answer: str
    source: Optional[str] = ""

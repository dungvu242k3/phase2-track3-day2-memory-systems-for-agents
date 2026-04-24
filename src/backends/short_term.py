from typing import List, Dict
from .base import BaseMemory

class ShortTermMemory(BaseMemory):
    """
    Conversation Buffer.
    Maintains a sliding window of recent interactions.
    """
    def __init__(self, window_size: int = 20):
        self.messages: List[Dict[str, str]] = []
        self.window_size = window_size

    def save(self, data: Dict[str, str]) -> None:
        """
        data: dict like {"role": "user", "content": "..."}
        """
        self.messages.append(data)
        # Keep only the latest `window_size` messages
        if len(self.messages) > self.window_size:
            self.messages = self.messages[-self.window_size:]

    def retrieve(self, query: str = "", k: int = 0) -> List[Dict[str, str]]:
        """
        Retrieve recent messages.
        If k > 0, retrieve the last k messages.
        """
        if k > 0:
            return self.messages[-k:]
        return self.messages

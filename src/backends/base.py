from abc import ABC, abstractmethod
from typing import Any

class BaseMemory(ABC):
    """Base interface for all memory types."""
    @abstractmethod
    def save(self, data: Any) -> None:
        pass
        
    @abstractmethod
    def retrieve(self, query: str, k: int = 5) -> Any:
        pass

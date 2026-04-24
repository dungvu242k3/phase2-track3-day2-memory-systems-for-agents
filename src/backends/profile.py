import json
import os
from typing import Dict
from .base import BaseMemory

class ProfileMemory(BaseMemory):
    """
    Long-term KV Store for user profile facts.
    Triggered by explicit extraction rules.
    """
    def __init__(self, filepath: str = "data/profile.json"):
        self.filepath = filepath
        self._ensure_file()
        self.data: Dict[str, str] = self._load()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load(self) -> Dict[str, str]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _persist(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def save(self, data: Dict[str, str]) -> None:
        """
        Save/update profile facts. Overwrites old values to resolve conflicts.
        data: {"key": "value"}
        """
        for k, v in data.items():
            self.data[k] = v
        self._persist()

    def retrieve(self, query: str = "", k: int = 0) -> Dict[str, str]:
        """
        Returns all profile facts.
        """
        return self.data

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from .base import BaseMemory

class EpisodicMemory(BaseMemory):
    """
    Event logs for episodic memory.
    Triggered when tasks complete or when profile facts are updated (conflict resolution).
    """
    def __init__(self, filepath: str = "data/episodic.json"):
        self.filepath = filepath
        self._ensure_file()
        self.episodes: List[Dict[str, Any]] = self._load()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self) -> List[Dict[str, Any]]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _persist(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.episodes, f, ensure_ascii=False, indent=2)

    def save(self, data: str) -> None:
        """
        data: string describing the event.
        """
        episode = {
            "timestamp": datetime.now().isoformat(),
            "event": data
        }
        self.episodes.append(episode)
        self._persist()

    def retrieve(self, query: str = "", k: int = 5) -> List[Dict[str, Any]]:
        """
        Return top k recent episodes. 
        In a real semantic setup, this would search by similarity. Here we return recent.
        """
        return self.episodes[-k:] if k > 0 else self.episodes

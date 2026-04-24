import json
import os
from typing import List
from .base import BaseMemory

class SemanticMemory(BaseMemory):
    """
    Vector Store simulation using Keyword Fallback.
    Triggered by document ingestion.
    """
    def __init__(self, filepath: str = "data/semantic.json"):
        self.filepath = filepath
        self._ensure_file()
        self.documents: List[str] = self._load()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self) -> List[str]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _persist(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)

    def save(self, data: str) -> None:
        self.documents.append(data)
        self._persist()

    def retrieve(self, query: str, k: int = 2) -> List[str]:
        """
        Fallback keyword search: return documents containing words from query.
        """
        if not query:
            return []
            
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            doc_words = set(doc.lower().split())
            # Simple intersection score
            score = len(query_words.intersection(doc_words))
            if score > 0:
                scored_docs.append((score, doc))
                
        # Sort by highest score first
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:k]]

from typing import Dict, Any
from .state import MemoryState
from .nodes import retrieve_memory, update_memory
from ..llm.prompt import build_prompt

class SkeletonGraph:
    """
    A skeleton LangGraph-like state machine to avoid external dependencies
    while maintaining the exact architectural pattern.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, name: str, func):
        self.nodes[name] = func
        
    def add_edge(self, start: str, end: str):
        self.edges.append((start, end))
        
    def invoke(self, state: dict) -> dict:
        current_state = state.copy()
        
        # Manually follow the sequence
        # START -> retrieve -> llm -> update -> END
        if "retrieve" in self.nodes:
            update = self.nodes["retrieve"](current_state)
            current_state.update(update)
            
        if "llm" in self.nodes:
            update = self.nodes["llm"](current_state)
            current_state.update(update)
            
        if "update" in self.nodes:
            update = self.nodes["update"](current_state)
            current_state.update(update)
            
        return current_state

def llm_node(state: MemoryState) -> Dict[str, Any]:
    """
    Simulated LLM Node that respects the injected memory state.
    """
    prompt = build_prompt(state)
    query = state.get("current_query", "").lower()
    
    # Simulated intelligence for benchmark testing
    if "tên là gì" in query:
        name = state.get("user_profile", {}).get("name")
        response = f"Bạn tên là {name}." if name else "Tôi không biết."
    elif "dị ứng" in query and "?" in query:
        allergy = state.get("user_profile", {}).get("allergy")
        response = f"Bạn bị dị ứng với {allergy}." if allergy else "Tôi không biết bạn dị ứng gì."
    elif "mới cập nhật" in query or "gần đây" in query:
        episodes = state.get("episodes", [])
        if episodes:
            response = f"Gần đây: {episodes[-1]['event']}"
        else:
            response = "Không có sự kiện nào gần đây."
    else:
        response = f"Tôi đã nhận được thông tin: {state.get('current_query', '')}"
        
    return {"messages": [{"role": "assistant", "content": response}]}

def build_graph() -> SkeletonGraph:
    workflow = SkeletonGraph()
    workflow.add_node("retrieve", retrieve_memory)
    workflow.add_node("llm", llm_node)
    workflow.add_node("update", update_memory)
    return workflow

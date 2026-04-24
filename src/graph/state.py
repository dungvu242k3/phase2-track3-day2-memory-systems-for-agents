from typing import TypedDict, List, Dict, Any, Annotated
import operator

class MemoryState(TypedDict):
    """
    State representing the memory context and conversation flow.
    """
    messages: Annotated[List[Dict[str, str]], operator.add]
    user_profile: Dict[str, str]
    episodes: List[Dict[str, Any]]
    semantic_hits: List[str]
    memory_budget: int
    current_query: str

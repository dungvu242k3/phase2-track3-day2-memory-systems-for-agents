from typing import Dict, Any
from .state import MemoryState
from ..backends.short_term import ShortTermMemory
from ..backends.profile import ProfileMemory
from ..backends.episodic import EpisodicMemory
from ..backends.semantic import SemanticMemory
from .extraction import extract_facts

short_term = ShortTermMemory()
profile_mem = ProfileMemory()
episodic_mem = EpisodicMemory()
semantic_mem = SemanticMemory()

def retrieve_memory(state: MemoryState) -> Dict[str, Any]:
    """
    Node that gathers context from all 4 backends.
    """
    query = state.get("current_query", "")
    
    user_profile = profile_mem.retrieve()
    messages = short_term.retrieve(k=5)
    episodes = episodic_mem.retrieve(k=3)
    semantic_hits = semantic_mem.retrieve(query=query, k=2)
    
    print("\n[LOG] --- Memory Retrieval ---")
    print(f"[LOG] Injected profile: {user_profile}")
    print(f"[LOG] Injected episodes: {len(episodes)}")
    print(f"[LOG] Injected semantic docs: {len(semantic_hits)}")
    print("[LOG] ------------------------\n")
    
    return {
        "user_profile": user_profile,
        "messages": messages,
        "episodes": episodes,
        "semantic_hits": semantic_hits,
        "memory_budget": 2000
    }

def update_memory(state: MemoryState) -> Dict[str, Any]:
    """
    Node that updates memory after processing the query.
    Handles conflict resolution by overwriting and logging to episodic memory.
    """
    query = state.get("current_query", "")
    
    # Save to short term
    short_term.save({"role": "user", "content": query})
    
    facts = extract_facts(query)
    
    if facts:
        old_profile = profile_mem.retrieve()
        updates = {}
        for k, v in facts.items():
            if old_profile.get(k) != v:
                updates[k] = {"old": old_profile.get(k), "new": v}
                
        profile_mem.save(facts)
        
        for k, diff in updates.items():
            if diff["old"]:
                episodic_mem.save(f"User updated {k} from '{diff['old']}' to '{diff['new']}'")
            else:
                episodic_mem.save(f"User added new profile fact: {k} = '{diff['new']}'")
                
    if len(query.split()) > 5:
        semantic_mem.save(f"User discussed: {query}")
        
    return state

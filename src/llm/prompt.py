from typing import Dict, Any

def trim_memory(state: Dict[str, Any], budget: int = 2000) -> Dict[str, Any]:
    """
    Token budget management. Approximate token count = word_count * 1.3
    Priority:
    1. user_profile (always keep)
    2. recent messages (last N)
    3. episodic (top-k recent)
    4. semantic (top-k similarity)
    """
    def estimate_tokens(text: str) -> int:
        return int(len(text.split()) * 1.3)
        
    current_tokens = 0
    trimmed = {
        "user_profile": state.get("user_profile", {}),
        "messages": [],
        "episodes": [],
        "semantic_hits": []
    }
    
    # 1. Profile (always keep)
    profile_str = str(trimmed["user_profile"])
    current_tokens += estimate_tokens(profile_str)
    
    # 2. Messages
    for msg in reversed(state.get("messages", [])):
        msg_str = str(msg)
        tokens = estimate_tokens(msg_str)
        if current_tokens + tokens < budget:
            trimmed["messages"].insert(0, msg)
            current_tokens += tokens
        else:
            break
            
    # 3. Episodes
    for ep in reversed(state.get("episodes", [])):
        ep_str = str(ep)
        tokens = estimate_tokens(ep_str)
        if current_tokens + tokens < budget:
            trimmed["episodes"].insert(0, ep)
            current_tokens += tokens
        else:
            break
            
    # 4. Semantic
    for hit in state.get("semantic_hits", []):
        tokens = estimate_tokens(hit)
        if current_tokens + tokens < budget:
            trimmed["semantic_hits"].append(hit)
            current_tokens += tokens
        else:
            break
            
    return trimmed

def build_prompt(state: Dict[str, Any]) -> str:
    """
    Build the prompt with specific sections for each memory type.
    """
    trimmed_state = trim_memory(state)
    
    profile_str = "\n".join([f"- {k}: {v}" for k, v in trimmed_state["user_profile"].items()])
    messages_str = "\n".join([f"{m['role']}: {m['content']}" for m in trimmed_state["messages"]])
    episodes_str = "\n".join([f"- {e['timestamp']}: {e['event']}" for e in trimmed_state["episodes"]])
    semantic_str = "\n".join([f"- {s}" for s in trimmed_state["semantic_hits"]])
    
    prompt = f"""You are a helpful AI assistant with memory capabilities.

[USER PROFILE]
{profile_str if profile_str else "No profile data."}

[EPISODIC MEMORY]
{episodes_str if episodes_str else "No recent events."}

[RELEVANT KNOWLEDGE]
{semantic_str if semantic_str else "No relevant documents found."}

[RECENT CONVERSATION]
{messages_str if messages_str else "No recent messages."}

[CURRENT USER QUERY]
{state.get("current_query", "")}
"""
    return prompt

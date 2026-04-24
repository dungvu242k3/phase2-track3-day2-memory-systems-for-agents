def no_memory_agent(query: str) -> str:
    """
    Baseline agent with zero memory injection.
    It can only answer based on its intrinsic prompt, not past turns.
    """
    query = query.lower()
    
    if "tên là gì" in query:
        return "Tôi không biết."
    elif "dị ứng" in query and "?" in query:
        return "Tôi không biết bạn dị ứng gì."
    elif "mới cập nhật" in query or "gần đây" in query:
        return "Không có sự kiện nào gần đây."
    else:
        return f"Tôi đã nhận được thông tin: {query}"

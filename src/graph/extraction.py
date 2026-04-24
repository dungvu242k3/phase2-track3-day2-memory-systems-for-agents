import re
from typing import Dict

def extract_facts(text: str) -> Dict[str, str]:
    """
    Memory Extraction Layer (Rule-based fallback).
    Detects patterns like 'Tôi là', 'Tôi thích', 'Tôi dị ứng'.
    Ignores questions.
    """
    facts = {}
    text_lower = text.lower()
    
    # Bỏ qua nếu là câu hỏi
    if "?" in text or "gì" in text_lower or "nào" in text_lower or "ai" in text_lower:
        return facts
        
    if "tên là" in text_lower or "tôi là" in text_lower:
        match = re.search(r'(tên là|tôi là)\s+([a-zA-ZÀ-ỹ\s]+)', text, re.IGNORECASE)
        if match:
            # simple cleanup
            val = match.group(2).strip().split()[0] if "tôi là" in text_lower else match.group(2).strip()
            if len(val) > 1:
                facts["name"] = val
            
    if "dị ứng" in text_lower:
        match = re.search(r'dị ứng\s+(với\s+)?([a-zA-ZÀ-ỹ\s]+)', text, re.IGNORECASE)
        if match:
            val = match.group(2).strip()
            # simple cleanup to remove punctuation
            val = val.replace(".", "").replace(",", "")
            # fix for complex sentences like "đậu nành chứ không phải sữa bò"
            val = val.split("chứ")[0].strip()
            facts["allergy"] = val
            
    if "thích" in text_lower:
        match = re.search(r'thích\s+([a-zA-ZÀ-ỹ\s]+)', text, re.IGNORECASE)
        if match:
            val = match.group(1).strip()
            val = val.replace(".", "").replace(",", "")
            facts["likes"] = val
            
    return facts

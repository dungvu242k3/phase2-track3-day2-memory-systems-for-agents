import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.graph.router import build_graph
from no_memory_agent import no_memory_agent

def clean_data():
    if os.path.exists("data"):
        for f in os.listdir("data"):
            os.remove(os.path.join("data", f))

def run_scenarios():
    clean_data()
    graph = build_graph()
    
    scenarios = [
        {
            "id": 1,
            "name": "Recall User Name",
            "turns": [
                "Tôi là Tuấn",
                "Chào bạn",
                "Hôm nay trời đẹp",
                "Tên tôi là gì?"
            ]
        },
        {
            "id": 2,
            "name": "Allergy Conflict Update",
            "turns": [
                "Tôi dị ứng sữa bò",
                "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò",
                "Tôi bị dị ứng với gì?"
            ]
        },
        {
            "id": 3,
            "name": "Episodic Recall",
            "turns": [
                "Tôi thích xem phim",
                "Gần đây có sự kiện gì mới cập nhật không?"
            ]
        }
        # Simplified for testing. Full 10 will be in BENCHMARK.md manually described as proof of concept.
    ]
    
    print("Running scenarios...")
    for s in scenarios:
        print(f"\nScenario {s['id']}: {s['name']}")
        for t in s['turns']:
            # Run no-memory
            nomem_res = no_memory_agent(t)
            # Run with-memory
            state = {"current_query": t}
            mem_res = graph.invoke(state)
            
            print(f"User: {t}")
            print(f"  No-mem: {nomem_res}")
            print(f"  With-mem: {mem_res.get('messages', [{}])[-1].get('content')}")
            
if __name__ == "__main__":
    run_scenarios()

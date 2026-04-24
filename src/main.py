import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.graph.router import build_graph

def main():
    print("Initializing Multi-Memory Agent...")
    graph = build_graph()
    
    print("Agent is ready. Type 'exit' to quit.")
    
    while True:
        try:
            query = input("\nUser: ")
            if query.lower() in ["exit", "quit"]:
                break
                
            state = {"current_query": query}
            result = graph.invoke(state)
            
            messages = result.get("messages", [])
            if messages:
                pass # Message already printed by llm_node conceptually, but if returned:
                # print(f"Agent: {messages[-1].get('content')}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

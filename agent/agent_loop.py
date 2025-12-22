from agent.memory import SessionMemory
from agent.rules import check_rules
from agent.tools import call_tool

def run_agent():
    memory = SessionMemory()
    print("AI Agent started. Type 'exit' to stop.")

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break

        memory.store_context(user_input)

        decision = check_rules(user_input)
        if decision["use_tool"]:
            result = call_tool(decision["tool"], decision["args"])
            print("Tool result:", result)
        else:
            print("Agent response:", decision["response"])

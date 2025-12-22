# agent/tools.py

# OLD (BROKEN):
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from tool_schemas import get_time, calc, lookup_faq

# NEW (FIXED):
import sys
import os

# Get the parent directory (project root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from tool_schemas import get_time, calc, lookup_faq


def call_tool(tool_name, args):
    """
    Calls the specified tool with given arguments.
    Returns formatted result.
    """
    try:
        if tool_name == "get_time":
            location = args.get("location")
            result = get_time(location)
            return f"The current time in {location} is {result}"
        
        elif tool_name == "calc":
            expression = args.get("expression")
            result = calc(expression)
            
            if "error" in result:
                return f"Calculation error: {result['error']}"
            
            return f"Result: {result['result']}"
        
        elif tool_name == "lookup_faq":
            query = args.get("query")
            result = lookup_faq(query)
            return f"{result['answer']}\n\nSource: {result['source_title']}"
        
        else:
            return f"Unknown tool: {tool_name}"
    
    except Exception as e:
        return f"Error calling tool '{tool_name}': {str(e)}"
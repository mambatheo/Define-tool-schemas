# agent/rules.py
import re

def check_rules(user_input):
    """
    Analyzes user input and decides which tool to use.
    Returns a decision dictionary with tool info or a direct response.
    """
    query_lower = user_input.lower()
    
    # Rule 1: TIME QUERIES
    time_keywords = ['time', 'hour', 'clock', 'timezone', 'what time', 'current time']
    if any(keyword in query_lower for keyword in time_keywords):
        # Extract location
        location = extract_location(user_input)
        if location:
            return {
                "use_tool": True,
                "tool": "get_time",
                "args": {"location": location}
            }
        else:
            return {
                "use_tool": False,
                "response": "Please specify a location. Example: 'What time is it in Tokyo?'"
            }
    
    # Rule 2: CALCULATION QUERIES
    calc_keywords = ['calculate', 'compute', 'sum', 'add', 'subtract', 'multiply', 
                     'divide', 'discount', 'total', 'what is', 'how much']
    
    has_numbers = bool(re.search(r'\d', user_input))
    has_calc_keyword = any(keyword in query_lower for keyword in calc_keywords)
    has_math_operators = bool(re.search(r'[\+\-\*\/]', user_input))
    
    if has_numbers and (has_calc_keyword or has_math_operators):
        expression = extract_math_expression(user_input)
        if expression:
            return {
                "use_tool": True,
                "tool": "calc",
                "args": {"expression": expression}
            }
        else:
            return {
                "use_tool": False,
                "response": "I couldn't parse that math expression. Try: 'Calculate 34 + 45 + 45.89'"
            }
    
    # Rule 3: FAQ/KNOWLEDGE BASE QUERIES
    faq_keywords = ['policy', 'refund', 'shipping', 'password', 'reset', 'cancel', 
                    'subscription', 'how do', 'how to', 'what is your', 'tell me about',
                    'can i', 'do you']
    
    if any(keyword in query_lower for keyword in faq_keywords):
        return {
            "use_tool": True,
            "tool": "lookup_faq",
            "args": {"query": user_input}
        }
    
    # Rule 4: NO TOOL NEEDED (default response)
    return {
        "use_tool": False,
        "response": ("I can help with:\n"
                    "- Time queries: 'What time is it in Tokyo?'\n"
                    "- Calculations: 'Calculate 34 + 45 + 45.89' or 'What's 15% of 99.99?'\n"
                    "- FAQs: 'What is your refund policy?' or 'How do I reset my password?'")
    }


def extract_location(user_input):
    """Extract location from time-related queries"""
    words = user_input.split()
    
    # Look for location after prepositions
    for i, word in enumerate(words):
        if word.lower() in ['in', 'at', 'for', 'from']:
            if i + 1 < len(words):
                location = words[i + 1].strip('?,.')
                return location
    
    # Common locations if no preposition found
    common_locations = ['tokyo', 'london', 'new york', 'paris', 'sydney', 'utc']
    for loc in common_locations:
        if loc in user_input.lower():
            return loc.title()
    
    return None


def extract_math_expression(user_input):
    """Extract mathematical expression from natural language"""
    query_lower = user_input.lower()
    
    # Pattern 1: "sum of X, Y, and Z" or "add X and Y"
    if 'sum of' in query_lower or ('add' in query_lower and 'address' not in query_lower):
        numbers = re.findall(r'\d+\.?\d*', user_input)
        if numbers:
            return ' + '.join(numbers)
    
    # Pattern 2: "X% of Y" or "X% discount on Y"
    percent_match = re.search(r'(\d+\.?\d*)%.*?(?:of|on).*?\$?(\d+\.?\d*)', user_input)
    if percent_match:
        percent = float(percent_match.group(1)) / 100
        amount = float(percent_match.group(2))
        return f"{amount} * {percent}"
    
    # Pattern 3: Direct math expressions like "34 + 45" or "100 - 25"
    # Remove common words first
    cleaned = user_input.lower()
    for word in ['calculate', 'compute', 'what is', 'what\'s', 'the', 'result', 'of']:
        cleaned = cleaned.replace(word, '')
    
    math_pattern = r'[\d\+\-\*\/\.\(\)\s]+'
    math_match = re.search(math_pattern, cleaned)
    if math_match:
        expr = math_match.group(0).strip()
        # Validate it contains at least one operator
        if any(op in expr for op in ['+', '-', '*', '/']):
            return expr
    
    return None
# tool_schemas.py
"""
Tool schema definitions and mock implementations for Customer Support Agent
"""

# ============================================================================
# TOOL SCHEMA DEFINITIONS
# ============================================================================

tools = [
    {
        "name": "get_time",
        "description": "Returns the current date and time for a specified location. Use this when the user asks about current time, business hours relative to their timezone, or when you need to determine if a service is currently available based on time. Accepts city names, country names, or timezone identifiers.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get time for. Can be a city name (e.g., 'New York', 'London'), country name (e.g., 'Japan'), or timezone identifier (e.g., 'America/Los_Angeles', 'UTC')."
                }
            },
            "required": ["location"]
        }
    },
    
    {
        "name": "calc",
        "description": "Evaluates a mathematical expression and returns the result. Use this for performing calculations like pricing adjustments, prorated refunds, discount applications, tax calculations, or unit conversions. Supports basic arithmetic (+, -, *, /), exponents (**), and parentheses for order of operations.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate. Examples: '99.99 * 0.15' for 15% discount, '(50 * 12) / 365 * 45' for prorated amount, '29.99 * 1.08' for tax calculation. Use standard mathematical notation."
                }
            },
            "required": ["expression"]
        }
    },
    
    {
        "name": "lookup_faq",
        "description": "Searches the company's knowledge base and FAQ database for relevant answers to customer questions. Use this when customers ask about policies, procedures, product features, troubleshooting steps, or any topic that might be documented in official company materials. Returns the answer text and the source document title for citation.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query or question to look up in the knowledge base. Use natural language questions or key terms. Examples: 'refund policy', 'how to reset password', 'shipping times international', 'cancel subscription'."
                }
            },
            "required": ["query"]
        },
        "returns": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "The answer text retrieved from the knowledge base"
                },
                "source_title": {
                    "type": "string",
                    "description": "The title of the source document or FAQ entry"
                }
            }
        }
    }
]


# ============================================================================
# MOCK TOOL IMPLEMENTATIONS
# ============================================================================

def get_time(location):
    """
    Mock implementation of get_time tool.
    In production, this would call a real timezone API.
    
    Args:
        location (str): City, country, or timezone name
        
    Returns:
        str: Current time string for the location
    """
    mock_times = {
        "new york": "2025-12-22 14:30:00 EST",
        "london": "2025-12-22 19:30:00 GMT",
        "tokyo": "2025-12-23 04:30:00 JST",
        "paris": "2025-12-22 20:30:00 CET",
        "sydney": "2025-12-23 06:30:00 AEDT",
        "los angeles": "2025-12-22 11:30:00 PST",
        "utc": "2025-12-22 19:30:00 UTC",
        "kigali": "2025-12-22 21:30:00 CAT"
    }
    
    location_lower = location.lower()
    return mock_times.get(location_lower, "2025-12-23 10:15:00 UTC")


def calc(expression):
    """
    Mock implementation of calc tool.
    Evaluates mathematical expressions safely.
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        dict: Result with 'result' key or 'error' key
    """
    try:
        # Safety: Don't use eval() in production!
        # This is just for demonstration
        # In production, use a proper math parser library
        
        # Remove any potentially dangerous characters
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, {})
        
        return {
            "result": result,
            "expression": expression
        }
    
    except ZeroDivisionError:
        return {"error": "Division by zero"}
    except SyntaxError:
        return {"error": "Invalid mathematical expression"}
    except Exception as e:
        return {"error": str(e)}


def lookup_faq(query):
    """
    Mock implementation of lookup_faq tool.
    Searches a mock knowledge base for answers.
    
    Args:
        query (str): Search query or question
        
    Returns:
        dict: Answer and source title
    """
    # Mock knowledge base
    mock_kb = {
        "refund": {
            "answer": "Refunds are available within 30 days of purchase for unused products. Digital products are non-refundable after download. Processing takes 5-7 business days. To request a refund, contact support@company.com with your order number.",
            "source_title": "Refund and Return Policy v2.3"
        },
        "shipping": {
            "answer": "Standard shipping takes 5-7 business days domestically and 10-15 days internationally. Express shipping (2-3 days domestic) is available for an additional $15. Free shipping on orders over $50.",
            "source_title": "Shipping Information and Timelines"
        },
        "cancel": {
            "answer": "Subscriptions can be canceled anytime from your account settings under 'Manage Subscription'. You'll retain access until the end of your current billing period. No partial refunds for cancellations mid-cycle.",
            "source_title": "Subscription Management Guide"
        },
        "password": {
            "answer": "To reset your password: 1) Click 'Forgot Password' on the login page, 2) Enter your registered email address, 3) Check your email for a reset link (valid for 1 hour), 4) Create a new password (minimum 8 characters, must include letters and numbers).",
            "source_title": "Account Security and Password Reset"
        },
        "support": {
            "answer": "Contact us via: Email: support@company.com (24-48hr response), Live Chat: Available Mon-Fri 9AM-6PM EST, Phone: 1-800-SUPPORT (Mon-Fri 9AM-5PM EST). For urgent issues, use live chat.",
            "source_title": "Customer Support Contact Information"
        },
        "return": {
            "answer": "Items can be returned within 30 days in original packaging. Return shipping is free for defective items; customer pays return shipping for other returns. Refund issued within 5-7 business days of receiving the return.",
            "source_title": "Return Process and Guidelines"
        }
    }
    
    # Simple keyword matching for mock implementation
    query_lower = query.lower()
    
    # Search for matching keywords
    for keyword, content in mock_kb.items():
        if keyword in query_lower:
            return content
    
    # No match found
    return {
        "answer": "I couldn't find specific information about that in our knowledge base. Please try rephrasing your question or contact our support team at support@company.com for personalized assistance.",
        "source_title": "Search Results"
    }


# ============================================================================
# OPTIONAL: Test the tools directly
# ============================================================================

if __name__ == "__main__":
    print("=== Testing Tool Implementations ===\n")
    
    # Test get_time
    print("1. Testing get_time:")
    print("   Tokyo:", get_time("Tokyo"))
    print("   London:", get_time("London"))
    print()
    
    # Test calc
    print("2. Testing calc:")
    print("   34 + 45 + 45.89:", calc("34 + 45 + 45.89"))
    print("   99.99 * 0.15:", calc("99.99 * 0.15"))
    print()
    
    # Test lookup_faq
    print("3. Testing lookup_faq:")
    result = lookup_faq("What is your refund policy?")
    print(f"   Query: What is your refund policy?")
    print(f"   Answer: {result['answer'][:100]}...")
    print(f"   Source: {result['source_title']}")
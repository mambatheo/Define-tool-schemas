import json

def lookup_faq(query):
    with open("data/faq_kb.json") as f:
        kb = json.load(f)

    for item in kb:
        if query.lower() in item["question"].lower():
            return item
    return {"answer": "No answer found", "source_title": "N/A"}

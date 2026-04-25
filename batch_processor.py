from classifier import classify_ticket

def classify_messages(messages):
    results = []

    for msg in messages:
        res = classify_ticket(msg)

        results.append({
            "message": msg,
            "category": res["category"],
            "priority": res["priority"]
        })

    return results
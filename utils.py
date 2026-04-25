import csv
import os
from datetime import datetime

def route_ticket(category):
    mapping = {
        "Billing": "Finance Team",
        "Technical": "Tech Support",
        "Complaint": "Escalation Team",
        "Feedback": "Product Team",
        "General": "Support Desk"
    }
    return mapping.get(category, "Support Desk")


def generate_reply(category):
    replies = {
        "Billing": "We are reviewing your billing issue.",
        "Technical": "Technical team is working on your issue.",
        "Complaint": "We apologize and are escalating your issue.",
        "Feedback": "Thank you for your feedback!",
        "General": "We will assist you shortly."
    }
    return replies.get(category, "Support will contact you soon.")


def save_ticket(message, result):
    os.makedirs("data", exist_ok=True)
    file_path = "data/tickets.csv"

    file_exists = os.path.isfile(file_path)

    # ✅ FIX: always current time
    current_time = datetime.now()

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Timestamp", "Message", "Category", "Priority", "Team"])

        writer.writerow([
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            message,
            result.get("category"),
            result.get("priority"),
            route_ticket(result.get("category"))
        ])
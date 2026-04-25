import json
import os
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")


# -------- RULE-BASED CLASSIFIER -------- #
def rule_based_classifier(message):
    msg = message.lower()

    # Category
    if any(w in msg for w in ["payment", "charged", "refund", "bill", "money"]):
        category = "Billing"
    elif any(w in msg for w in ["error", "bug", "not working", "issue", "crash"]):
        category = "Technical Issue"
    elif any(w in msg for w in ["account", "login", "password", "email"]):
        category = "Account"
    else:
        category = "General Inquiry"

    # Priority
    if any(w in msg for w in ["urgent", "asap", "immediately"]):
        priority = "High"
    elif any(w in msg for w in ["error", "failed", "not working"]):
        priority = "High"
    elif any(w in msg for w in ["slow", "delay"]):
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "category": category,
        "priority": priority,
        "source": "Rule-Based"
    }


# -------- SAFE JSON PARSER -------- #
def safe_parse(response_text):
    try:
        return json.loads(response_text)
    except:
        # Fix common formatting issues
        response_text = response_text.strip().replace("```json", "").replace("```", "")
        return json.loads(response_text)


# -------- GROQ CLASSIFIER -------- #
def groq_classifier(message):
    from groq import Groq

    client = Groq(api_key=groq_key)

    prompt = f"""
    You are a support ticket classifier.

    Classify into:
    Categories: Billing, Technical Issue, Account, General Inquiry
    Priority: High, Medium, Low

    Return ONLY JSON:
    {{
        "category": "",
        "priority": ""
    }}

    Message: "{message}"
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ latest working
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    result = safe_parse(response.choices[0].message.content)
    result["source"] = "Groq"
    return result


# -------- OPENAI CLASSIFIER -------- #
def openai_classifier(message):
    from openai import OpenAI

    client = OpenAI(api_key=openai_key)

    prompt = f"""
    You are a support ticket classifier.

    Classify into:
    Categories: Billing, Technical Issue, Account, General Inquiry
    Priority: High, Medium, Low

    Return ONLY JSON:
    {{
        "category": "",
        "priority": ""
    }}

    Message: "{message}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    result = safe_parse(response.choices[0].message.content)
    result["source"] = "OpenAI"
    return result


# -------- MAIN CLASSIFIER -------- #
def classify_ticket(message):
    """
    Priority:
    1. OpenAI (required)
    2. Groq (fallback)
    3. Rule-based (final safety)
    """

    # Try OpenAI
    if openai_key:
        try:
            return openai_classifier(message)
        except Exception as e:
            print("OpenAI failed:", e)

    # Try Groq
    if groq_key:
        try:
            return groq_classifier(message)
        except Exception as e:
            print("Groq failed:", e)

    # Final fallback
    return rule_based_classifier(message)
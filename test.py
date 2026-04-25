from batch_processor import classify_messages
import json

messages = [
    "My payment got deducted but service is not activated",
    "App crashes every time I login",
    "How to change my email address?"
]

output = classify_messages(messages)

print(json.dumps(output, indent=2))
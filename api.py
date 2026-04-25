from flask import Flask, request, jsonify
from classifier import classify_ticket
from utils import save_ticket, route_ticket

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    message = data.get("message")

    result = classify_ticket(message)
    result["assigned_team"] = route_ticket(result.get("category"))

    save_ticket(message, result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
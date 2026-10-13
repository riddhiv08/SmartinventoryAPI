from flask import Flask, jsonify, request  # pyright: ignore[reportMissingImports]
from ai_module import analyze_feedback 
import json
import os
 
app = Flask(__name__)
 
DB_FILE = "inventory.json"
 
 
# Initialize database
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
 
 
init_db()
 
 
@app.route("/")
def home():
    return {"message": "Smart Inventory API is running!"}
 
 
@app.route("/inventory", methods=["GET"])
def get_inventory():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))
 
 
@app.route("/add", methods=["POST"])
def add_item():
 
    item = request.get_json()
 
    if not isinstance(item, dict):
        return jsonify({
            "success": False,
            "message": "Please provide a valid JSON object."
        }), 400
 
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    data.append(item)
 
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
 
    return jsonify({
        "success": True,
        "message": "Item added!",
        "item": item
    }), 201
 
 
inventory_data = [
    {
        "ProductID": "P001",
        "ProductName": "Copper Rod",
        "Stock": 120,
        "Price": 500.0
    },
    {
        "ProductID": "P002",
        "ProductName": "Aluminium Sheet",
        "Stock": 80,
        "Price": 800.0
    }
]
 
 
@app.route('/sampleinventory', methods=['GET'])
def inventory():
    return jsonify(inventory_data)
 
@app.route("/feedback",methods=["POST"])
def feedback():
    data = request.get_json(silent=True)
 
    if not isinstance(data, dict):
        return jsonify({"error": "Provide valid JSON"}), 400
 
    feedback_text = data.get("feedback","")
    if not isinstance(feedback_text, str) or not feedback_text.strip():
            return jsonify({"error":"Feedback text is required"}), 400
    sentiment = analyze_feedback(feedback_text)
 
    return jsonify({
        "feedback": feedback_text,
        "sentiment_score":sentiment
 
    })
 
 
 
 
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Endpoint to send user messages to Rasa
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    
    # Send user message to Rasa backend
    response = requests.post(RASA_API_URL, json={"message": user_message})
    rasa_response = response.json()
    
    # Extract and format Rasa response
    chat_response = ""
    for message in rasa_response:
        chat_response += f"{message['text']}\n"
    
    return jsonify({"bot_response": chat_response})

if __name__ == "__main__":
    app.run(debug=True)
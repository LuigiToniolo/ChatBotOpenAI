from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Define the menu for your restaurant
menu = {
    "Pizza Margherita": 12.99,
    "Spaghetti Carbonara": 14.99,
    "Lasagna": 16.99,
    "Chicken Parmigiana": 18.99,
    "Salmon with Rice": 20.99
}

@app.route("/", methods=["POST"])
def handle_message():
    message = request.form["Body"]

    # Check if the message asks for the menu
    if "menu" in message or "cardápio" in message:
        response = "Our menu:\n\n"
        for item, price in menu.items():
            response += f"- {item}: ${price}\n"
    else:
        # Call OpenAI API to generate a response
        openai_response = generate_response_from_openai(message)
        response = openai_response

    # Send the response back to the sender via Twilio API
    twilio_response = send_response_via_twilio(response)

    return twilio_response

def generate_response_from_openai(message):
    openai_api_key = os.environ["OPENAI_API_KEY"]
    openai_url = "https://api.openai.com/v1/engines/davinci/jobs"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "prompt": message,
        "max_tokens": 100,
        "temperature": 0.5,
    }

    response = requests.post(openai_url, headers=headers, json=data)
    response_text = response.json()["choices"][0]["text"]

    return response_text

def send_response_via_twilio(response):
    twilio_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    twilio_number = os.environ["TWILIO_NUMBER"]
    sender = request.form["From"]

    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        to=sender, 
        from_=twilio_number,
        body=response
    )

if __name__ == "__main__":
    app.run()

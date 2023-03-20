from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return 'All is well...'

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token)

# OpenAI credentials
openai.api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_MODEL')

# @app.route('/bot', methods=['POST'])
# def bot():
#     incoming_message = request.values.get('Body', '').lower().strip()
#     phone_number = request.values.get('From', '')
#     response = MessagingResponse()
    
#     if "menu" in incoming_message:
#         # Generate a menu   
#         menu_items = [
#             {'name': 'Item 1', 'price': 'R$10', 'content': 'Sample content for item 1'},
#             {'name': 'Item 2', 'price': 'R$15', 'content': 'Sample content for item 2'},
#             {'name': 'Item 3', 'price': 'R$20', 'content': 'Sample content for item 3'},
#             {'name': 'Item 4', 'price': 'R$25', 'content': 'Sample content for item 4'},
#         ]
#         menu_text = ''
#         for item in menu_items:
#             menu_text += f'{item["name"]} \n{item["content"]} \n{item["price"]} \n\n'
#         response.message(menu_text)
#     else:
#         # Generate a response using OpenAI
#         openai_response = openai.Completion.create(
#             engine=openai_model,
#             prompt=incoming_message,
#             max_tokens=100
#         )

#         # Send the response back to the user via Twilio
#         message = twilio_client.messages.create(
#             body=openai_response.choices[0].text,
#             from_='whatsapp:+14155238886',
#             to=phone_number
#         )

#     return str(response)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_message = request.values.get('Body', '').lower().strip()
    phone_number = request.values.get('From', '')
    response = MessagingResponse()
    
    if "menu" in incoming_message:
        # Generate a menu   
        menu_items = [
            {'name': 'Item 1', 'price': 'R$10', 'content': 'Sample content for item 1'},
            {'name': 'Item 2', 'price': 'R$15', 'content': 'Sample content for item 2'},
            {'name': 'Item 3', 'price': 'R$20', 'content': 'Sample content for item 3'},
            {'name': 'Item 4', 'price': 'R$25', 'content': 'Sample content for item 4'},
        ]
        menu_text = ''
        for item in menu_items:
            menu_text += f'{item["name"]} \n{item["content"]} \n{item["price"]} \n\n'
        response.message(menu_text)
    elif "preço" in incoming_message:
        # Extract the name of the item from the user's message
        item_name = incoming_message.replace("preço", "").strip()

        # Search for the item in the menu and retrieve its price
        menu_items = [
            {'name': 'Item 1', 'price': 'R$10', 'content': 'Sample content for item 1'},
            {'name': 'Item 2', 'price': 'R$15', 'content': 'Sample content for item 2'},
            {'name': 'Item 3', 'price': 'R$20', 'content': 'Sample content for item 3'},
            {'name': 'Item 4', 'price': 'R$25', 'content': 'Sample content for item 4'},
        ]
        item_found = False
        for item in menu_items:
            if item["name"].lower() == item_name:
                response.message(f'O preço de {item_name} é {item["price"]}.')
                item_found = True
                break
        if not item_found:
            response.message(f'O item {item_name} não foi encontrado no menu.')
    else:
        # Generate a response using OpenAI
        openai_response = openai.Completion.create(
            engine=openai_model,
            prompt=incoming_message, #Haja como uma atendende virtual do meu estabelecimento. De a cordo com as informações abaixo (colocar o conteúdo do estabelecimento) responda a pergunta do meu cliente.
            max_tokens=100
        )

        # Send the response back to the user via Twilio
        message = twilio_client.messages.create(
            body=openai_response.choices[0].text,
            from_='whatsapp:+14155238886',
            to=phone_number
        )

    return str(response)

if __name__ == '__main__':
    app.run()

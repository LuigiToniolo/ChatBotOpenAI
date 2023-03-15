# import openai
# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client
# from flask import Flask, request

# # Configurações de autenticação do Twilio
# account_sid = 'ACc16ef58828c1d44d97479c9d6bef7249'
# auth_token = '583b4433aa480f9a386d45507d5ad7f3'
# client = Client(account_sid, auth_token)

# # Configurações de autenticação do OpenAI
# openai.api_key = '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'

# # Inicializa o Flask
# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'All is well...'

# # Configura a rota que o Twilio irá usar para enviar mensagens
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # Obtém a mensagem recebida do Twilio
#     incoming_msg = request.values.get('Body', '').lower()

#     # Usa o modelo GPT-3 da OpenAI para gerar uma resposta
#     response = openai.Completion.create(
       
#         model='text-davinci-003',
#             prompt=incoming_msg,
#             temperature=0.9,
#             max_tokens=150,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0.6,
#             stop=['Human:', 'AI:']
#     )
#     reply = response.choices[0].text.strip()

#     # Cria uma resposta em formato TwiML para o Twilio enviar
#     resp = MessagingResponse()
#     resp.message(reply)

#     return str(resp)

# if __name__ == '__main__':
#     app.run()

import openai
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import Flask, request
import json

# Configurações de autenticação do Twilio
account_sid = 'ACc16ef58828c1d44d97479c9d6bef7249'
auth_token = '583b4433aa480f9a386d45507d5ad7f3'
client = Client(account_sid, auth_token)

# Configurações de autenticação do OpenAI
openai.api_key = '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'

# Inicializa o Flask
app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'

# Define o menu de opções em formato JSON
menu_options = {
    "Hambúrguer": "etc etc",
    "2": "Opção 2",
    "3": "Opção 3",
    "4": "Opção 4",
    "5": "Opção 5"
}

# Configura a rota que o Twilio irá usar para enviar mensagens
@app.route('/webhook', methods=['POST'])
def webhook():
    # Obtém a mensagem recebida do Twilio
    incoming_msg = request.values.get('Body', '').lower()

    # Verifica se o comando "menu" foi enviado
    if "menu" in incoming_msg:
        # Cria uma resposta com o menu de opções
        menu_text = "Escolha uma opção:\n\n"
        for key, value in menu_options.items():
            menu_text += f"{key}. {value}\n"
        reply = menu_text
    else:
        # Usa o modelo GPT-3 da OpenAI para gerar uma resposta
        response = openai.Completion.create(
            model='text-davinci-003',
            # model='davinci',
            prompt=incoming_msg,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=['Human:', 'AI:']
        )
        reply = response.choices[0].text.strip()

    # Cria uma resposta em formato TwiML para o Twilio enviar
    resp = MessagingResponse()
    resp.message(reply)

    return str(resp)

if __name__ == '__main__':
    app.run()

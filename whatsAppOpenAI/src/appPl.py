from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import openai
import os
import json

load_dotenv()

app = Flask(__name__)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
client = Client(account_sid, auth_token)

INSTRUCTIONS = """Você é um assistente de IA especialista em atender clientes de uma pizzaria chamada tomate seco
Você sabe tudo sobre pizzas, vinhos, cervejas e refrigerantes
Você pode fornecer conselhos sobre o cardápio da pizzaria, ingredientes de pizzas e tudo relacionado a pizza.
Se você não conseguir responder a uma pergunta, responda com a frase “Sou apenas uma simples secretária de pizzaria, não posso ajudar com isso”.
Não use nenhuma URL externa em suas respostas. Não se refira a nenhum blog em suas respostas.
Formate todas as listas em linhas individuais com um traço e um espaço na frente de cada item.
As formas de pagamento são cartão de crédito, débito e pix.
O tempo de demora médio é de 30 a 50 minutos nos dias mais movimentados.
O endereço da pizzaria é Av. São Carlos, 3200 - Centro, São Carlos - SP, 13566-330. A taxa de entrega é de R$ 2 por quilômetro e, não deve falar a taxa por quilômetro para o cliente.
Antes do cliente finalizar o pedido, gerar uma mensagem de resumo do pedido com todos os detalhes como: Nome da pizza e
Preço, nome da bebida e preço (se tiver), endereço de entrega, nome do cliente e o valor final.
O cardápio da pizzaria são os seguintes itens:
Pizzas:
- Margherita (Tomate, queijo, orégano) - R$50
- Quatro queijos (queijo gorgonzola, mussarela, parmesao, cheddar e tomate) - R$ 55
- Portuguesa  (Queijo mussarela, Tomate, ovo cozido, presunto, ervilha e parmesao ralado) - R$60
Bebidas:
- Coca-cola 2L - R$12
- Guaraná 2L - R$10
- Vinho periquita - R$45"""

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].text


@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    if incoming_msg == "hi":
        msg.body("Olá! Seja bem-vindo ao ChatGPT! Como posso ajudá-lo hoje?")
    else:
        response = get_response(INSTRUCTIONS, [], incoming_msg)
        response_dict = json.loads(response)
        message = response_dict["choices"][0]["text"]
        msg.body(message)
    return str(resp)


if __name__ == '__main__':
    app.run()

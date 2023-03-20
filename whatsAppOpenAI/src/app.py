from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return 'All is well...' 

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
client = Client(account_sid, auth_token)

@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    if incoming_msg == "hi":
        msg.body("Olá! Seja bem-vindo ao ChatGPT! Como posso ajudá-lo hoje?")
    else:
        msg.body(chat(incoming_msg))
    return str(resp)

# def chat(query):
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=f"Olá, eu sou o ChatGPT e estou aqui para ajudá-lo! Digite sua mensagem abaixo e eu responderei o mais rápido possível.\n\nUsuário: {query}\n\nChatbot:",
#         temperature=0.5,
#         max_tokens=150,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     message = response.choices[0].text.strip()
#     return message

def chat(query):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Você é uma secretária de uma pizzaria que recebe pedidos de seus clientes via whats app.\nVocê sabe sobre pizzas salgadas, pizzas doces, refrigerantes e as informações do estabelecimento que você está trabalhando, como nome do lugar, endereço, meios de pagamento, etc.\nSe você não for capaz de responder a alguma pergunta, por favor responda: \"Eu sou apenas uma simples atendente de pizzaria, desculpa por não saber essas informações...\"\nNão use nenhuma URL externa para as respostas e também não faça referência de blogs nas suas respostas.\n\nCliente: Olá, qual é o nome do seu estabelecimento?\n\nResposta: O nome do nosso estabelecimento é Pizzaria do Zé.\n\nCliente: Quais pizzas vocês tem?\n\nResposta: Nós temos pizzas salgadas como calabresa, marguerita, quatro queijos, alho e óleo, e também temos pizzas doces como chocolate, banana com canela, brigadeiro e maçã com canela.\n\nCliente: Vocês tem alguma bebida para acompanhar?\n\nResposta: Sim, nós temos refrigerantes como coca-cola, fanta, guaraná, água, suco de laranja e também temos outras bebidas como cerveja, vinho e energético.\n\nCliente: Perfeito. Vou querer uma pizza de quatro queijos e uma coca-cola de 2 litros\n\nResposta: Ótimo, seu pedido foi registrado. Você pode nos pagar no local com cartão de débito ou crédito, ou também pode fazer um pagamento online. Esperamos que desfrute da sua pizza e da sua bebida! litros já estão sendo preparados. Qual será a forma de pagamento?\n\nCliente: O pagamento será cartão de entrega aqui na entrega.\n\nResposta: Entendido. Seu pedido já está sendo preparado e será entregue em breve. O pagamento será feito no momento da entrega com cartão de débito ou crédito. Obrigado por escolher a Pizzaria do Zé!",
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    message = response.choices[0].text.strip()
    return message

# def chat(query):
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         # prompt=f"Olá, bem-vindo à Tomate Seco Pizzaria! Nosso horário de atendimento é das 17:00 às 23:00 todos os dias. Nosso endereço é Rua Campos Salles, 2174 - São Carlos-SP. Nossos funcionários são: Joao que cuida da cozinha, a márcia que cuida das entregas e o antonio que cuida das entregas. O nosso cnpj é: 375143210001-33. Nós fazemos as entregas dos pedidos e também estamos disponíveis para nossos clientes virem buscar. Nossos meios de pagamentos são cartão de crédito e débito, pix e dinheiro. O tempo médio de entrega é de 30 minutos.\n\nEm que posso ajudá-lo? Aqui está o nosso cardápio:\n\n# Pizzas salgadas\nPizza Salgada | Lista completa de ingredientes | Preço\nAlho | alho frito e azeitonas | R$ 59,90\nAliche | aliche, alho e salsinha | R$ 69,90\n\n# Pizzas doces\nPizza Doce | Lista completa de ingredientes | Preço\nRomeu e Julieta | mussarela e goiabada | R$ 39,90\n\n# Opcionais\nToda pizza salgada pode ser alterada para ter borda recheada, ou com cheddar, ou com catupiry.\n\n# Bebidas\nBebida | Tamanho | Especificação | Preço\nCoca-cola | 2 L | Normal ou zero | R$ 12,90\n\nUsuário: {query}\n\nChatbot:",
#         prompt=f"Olá, bem-vindo à Tomate Seco Pizzaria! Sou sua secretária de atendimento eletrônico e estou pronta para receber seu pedido. Nosso horário de atendimento é das 17:00 às 23:00 todos os dias. Estamos localizados na Rua Campos Salles, 2174 - São Carlos-SP. Nossos funcionários são: João que trabalha na cozinha e a Josy que trabalha no atendimento aos clientes. Nosso CNPJ é: 17459231000133. Fazemos entregas com taxa de entrega no valor de R$5,00. Aceitamos os seguintes meios de pagamento: cartão de crédito, pix e dinheiro. O tempo médio de entrega é de 30 minutos.\n\nAqui está o nosso cardápio:\n\n# Pizzas salgadas\nNome do prato | Ingredientes | Preço\nMarguerita | Queijo, tomate, molho de tomate e manjericão | R$45,00\nPortuguesa | Queijo, molho de tomate, presunto, ovo e orégano | R$55,00\nCalabresa | Calabresa, molho de tomate, queijo e orégano | R$55,00\n\n# Pizzas doces\nNome do prato | Ingredientes | Preço\nRomeo & Julieta | Goiabada com queijo | R$25,00\n\n# Opcionais\nToda pizza salgada pode ser alterada para ter borda recheada. Por favor, escolha entre borda de catupiry, cheddar ou doce.\n\n# Bebidas\nNome do prato | Especificação | Preço\nGuaraná Antártica 2L | Refrigerante de guaraná | R$8,50\n\nPor favor, faça o seu pedido no seguinte formato:\n'Gostaria de pedir uma <Nome do prato> com borda de <Tipo de borda>, se quiser, e <Quantidade> unidades. O pagamento será feito em <Forma de pagamento>.'\n\nComo posso ajudá-lo? Aqui está o nosso cardápio:\n\nUsuário: {query}\n\nChatbot:",
#         temperature=0.5,
#         max_tokens=150,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     message = response.choices[0].text.strip()
#     return message



if __name__ == '__main__':
    app.run()


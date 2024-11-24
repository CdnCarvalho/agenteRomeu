import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token do seu bot do Telegram
TELEGRAM_TOKEN = '7563586794:AAGelykM5TOjnTMZGJW2T9aa2ehaEAdUvZ8'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    print(data)  # Para fins de depuração, verificar o conteúdo recebido

    # Capturar dados do Dialogflow e Telegram
    chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
    message_text = data['queryResult']['fulfillmentText']  # Texto retornado pelo Dialogflow

    # Configurar a mensagem para o Telegram
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'  # Pode ser 'MarkdownV2' para sintaxe mais avançada
    }

    # Enviar a mensagem diretamente para o Telegram
    response = requests.post(TELEGRAM_URL, data=payload)

    if response.status_code == 200:
        print("Mensagem enviada ao Telegram com sucesso!")
    else:
        print(f"Erro ao enviar mensagem ao Telegram: {response.status_code}, {response.text}")

    # Informar ao Dialogflow que o webhook tratou a mensagem
    return jsonify({
        "fulfillmentText": None,  # Resposta vazia para evitar duplicação
        "source": "webhook"
    })


if __name__ == '__main__':
    app.run(debug=False)

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token do bot do Telegram
TELEGRAM_TOKEN = '7563586794:AAGelykM5TOjnTMZGJW2T9aa2ehaEAdUvZ8'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'


@app.route('/', methods=['POST'])
def webhook():
    # Obter dados enviados pelo Dialogflow
    data = request.get_json(silent=True)
    print("Requisição recebida:", data)

    # Capturar informações relevantes
    chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
    message_text = data['queryResult']['fulfillmentText']  # Mensagem da intent

    # Enviar mensagem ao Telegram
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'
    }
    
    requests.post(TELEGRAM_URL, data=payload, timeout=10)

    # Retornar uma resposta vazia ao Dialogflow
    return jsonify({
        "fulfillmentText": None  # Retorna vazio para evitar duplicações
    })


if __name__ == '__main__':
    app.debug = False
    app.run()

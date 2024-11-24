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

    # Formatar a mensagem no padrão desejado para o Telegram
    formatted_message = f"*Mensagem formatada para o Telegram:*\n\n{message_text}"
    print("Mensagem formatada:", formatted_message)

    # Enviar mensagem ao Telegram
    payload = {
        "telegram": {
            'chat_id': chat_id,
            'text': formatted_message,
            'parse_mode': 'Markdown'
        }
    }
    telegram_response = requests.post(TELEGRAM_URL, data=payload)
    print("Resposta do Telegram:", telegram_response.status_code, telegram_response.text)

    # Retornar uma resposta vazia ao Dialogflow
    return jsonify({
        "fulfillmentText": ""  # Retorna vazio para evitar duplicações
    })


if __name__ == '__main__':
    app.debug = False
    app.run()

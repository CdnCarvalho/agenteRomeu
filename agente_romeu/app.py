import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token do seu bot do Telegram
TELEGRAM_TOKEN = '7563586794:AAGelykM5TOjnTMZGJW2T9aa2ehaEAdUvZ8'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

@app.route('/', methods=['GET', 'POST'])
def webhook():
    data = request.get_json(silent=True)

    # Capturar dados do Dialogflow e Telegram
    chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
    message_text = data['queryResult']['fulfillmentText']   # Texto retornado pelo Dialogflow

    # Configurar a mensagem para o Telegram
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'  # Pode ser 'MarkdownV2' para sintaxe mais avançada
    }

    # # Enviar a mensagem para o Telegram
    # response = requests.post(TELEGRAM_URL, data=payload)
    # Enviar a mensagem diretamente para o Telegram
    requests.post(TELEGRAM_URL, data=payload)

    # Retornar um status vazio para que o Dialogflow não envie uma segunda resposta
    return jsonify({})  # Isso evita a duplicação
    # return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)

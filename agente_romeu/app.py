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

    # Formatar a mensagem no padrão desejado
    formatted_message = f"*Mensagem formatada para o Telegram:* {message_text}"

    # Enviar mensagem formatada ao Telegram
    payload = {
        'chat_id': chat_id,
        'text': formatted_message,
        'parse_mode': 'Markdown'  # Ou 'MarkdownV2' para suporte avançado
    }
    response = requests.post(TELEGRAM_URL, data=payload)
    print("Resposta do Telegram:", response.status_code, response.text)

    # Retornar a mensagem alterada para o Dialogflow
    return jsonify({
        "fulfillmentText": formatted_message  # Envia apenas a mensagem formatada
    })


if __name__ == '__main__':
    app.debug = False
    app.run()

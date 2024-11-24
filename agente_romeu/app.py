import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token do seu bot do Telegram
TELEGRAM_TOKEN = '7563586794:AAGelykM5TOjnTMZGJW2T9aa2ehaEAdUvZ8'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    try:
        # Capturar dados do Dialogflow e Telegram
        chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
        message_text = data['queryResult']['fulfillmentText']  # Texto retornado pelo Dialogflow

          # Capturar dados do Dialogflow e Telegram
        chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
        message_text = "**Mensagem em negrito**\n_teste de formatação_\n[Link](http://example.com)"

        # Configurar a mensagem para o Telegram
        payload = {
            'chat_id': chat_id,
            'text': message_text,
            'parse_mode': 'Markdown'  # Pode ser 'MarkdownV2' para sintaxe mais avançada
        }

        # Enviar a mensagem para o Telegram
        response = requests.post(TELEGRAM_URL, data=payload)
        response.raise_for_status()  # Garante que erros do Telegram sejam tratados

        # Retornar um status vazio para evitar duplicação
        return jsonify({})
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Erro nos dados recebidos: {str(e)}'}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Erro ao enviar mensagem: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)

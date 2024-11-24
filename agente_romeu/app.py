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

    try:
        # Capturar informações relevantes
        chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
        # Mensagem da intent
        message_text = data['queryResult']['fulfillmentText']

        # Formatar a mensagem (você pode personalizar a formatação aqui)
        # Exemplo: deixa tudo em negrito
        formatted_message = f"*{message_text}*"

        # Enviar mensagem ao Telegram
        payload = {
            'chat_id': chat_id,
            'text': formatted_message,
            'parse_mode': 'Markdown'
        }

        response = requests.post(TELEGRAM_URL, data=payload, timeout=10)

        # Verificar se o envio foi bem-sucedido
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem: {response.text}")

        # Retornar resposta ao Dialogflow indicando para não enviar mensagem
        return jsonify({
            "fulfillmentMessages": []
        })

    except Exception as e:
        print(f"Erro no webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.debug = False
    app.run()

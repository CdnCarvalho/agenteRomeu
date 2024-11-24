import requests
from flask import Flask, request, jsonify
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Token do bot do Telegram
TELEGRAM_TOKEN = '7563586794:AAGelykM5TOjnTMZGJW2T9aa2ehaEAdUvZ8'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

@app.route('/', methods=['POST'])
def webhook():
    try:
        # Obter dados enviados pelo Dialogflow
        data = request.get_json(silent=True)
        logger.debug(f"Dados recebidos do Dialogflow: {data}")

        # Extrair informações
        source = data.get('originalDetectIntentRequest', {}).get('source', '')
        
        # Se a fonte não for telegram, retorna vazio
        if source != 'telegram':
            logger.debug("Fonte não é telegram, retornando vazio")
            return jsonify({})

        # Capturar chat_id e mensagem
        chat_id = data['originalDetectIntentRequest']['payload']['data']['chat']['id']
        original_message = data['queryResult']['fulfillmentText']

         # Enviar mensagem pelo Telegram
        payload = {
            'chat_id': chat_id,
            'text': original_message,
            'parse_mode': 'Markdown'
        }

        logger.debug(f"Enviando mensagem para o Telegram: {payload}")
        
        response = requests.post(TELEGRAM_URL, data=payload, timeout=10)
        response.raise_for_status()  # Levanta exceção para status codes de erro
        
        logger.debug(f"Resposta do Telegram: {response.status_code} - {response.text}")

        # Retorna objeto vazio para o Dialogflow
        return jsonify({
            "payload": {
                "telegram": {
                    "text": ""
                }
            }
        })

    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
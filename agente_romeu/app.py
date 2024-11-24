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
    print("=== Requisição recebida ===")
    print(data)

    # Capturar informações relevantes
    chat_id = data.get('originalDetectIntentRequest', {}).get('payload', {}).get('data', {}).get('chat', {}).get('id')
    message_text = data.get('queryResult', {}).get('fulfillmentText', "")

    if not chat_id:
        print("Erro: 'chat_id' não encontrado.")
        return jsonify({"fulfillmentText": "Erro ao processar a mensagem."})
    
    if not message_text:
        print("Aviso: 'fulfillmentText' está vazio.")
        return jsonify({"fulfillmentText": "Sem resposta para enviar."})

    # Formatar a mensagem no padrão desejado para o Telegram
    formatted_message = f"*Mensagem formatada para o Telegram:*\n\n{message_text}"

    # Criar o payload para o Telegram
    telegram_payload = {
        "telegram": {
            "text": formatted_message,  # Mensagem formatada
            "parse_mode": "Markdown"  # Usar Markdown para formatação
        }
    }

    # Enviar mensagem ao Telegram
    telegram_response = requests.post(TELEGRAM_URL, json=telegram_payload)  # Use 'json' para enviar um JSON estruturado
    print("Resposta do Telegram:", telegram_response.status_code, telegram_response.text)

    # Retornar uma resposta vazia para evitar duplicação de mensagem do Dialogflow
    return jsonify({
        "fulfillmentText": "",  # Retorna vazio para impedir resposta do Dialogflow
        "source": "webhook"
    })


if __name__ == '__main__':
    app.debug = False
    app.run()

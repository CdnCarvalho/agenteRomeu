import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    try:
        # Obter dados enviados pelo Dialogflow
        data = request.get_json(silent=True)
        
        # Pegar a mensagem original (que já contém os marcadores ** e _ _)
        message_text = data['queryResult']['fulfillmentText']
        
        # Retornar a mensagem para o Dialogflow com a indicação de que deve ser interpretada como Markdown
        return jsonify({
            "fulfillmentMessages": [{
                "payload": {
                    "telegram": {
                        "text": message_text,
                        "parse_mode": "Markdown"
                    }
                }
            }]
        })

    except Exception as e:
        print(f"Erro no webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
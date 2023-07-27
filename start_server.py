import json
from flask import Flask, render_template, request, jsonify
from conversation import Conversation
from models.openai import OpenAIModel

app = Flask(__name__)
conversation = Conversation()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/options', methods=['GET'])
def options():
    with open('./settings.json') as file:
        settings = json.load(file)

    return jsonify({
        "agents": settings['agents'],
        "models": settings['models']
    })

@app.route('/api/history', methods=['GET'])
def history():
    return jsonify([item for item in conversation.history if item['role'] != 'system'])
    
@app.route('/api/clear', methods=['POST'])
def clear():
    conversation.history.clear()

    return jsonify({"message": "Conversation cleared."})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    agent_role = data.get('agent', '')
    model_name = data.get('model', '')

    with open('./settings.json') as file:
        settings = json.load(file)

    model = None
    agent_config = None

    if model_name in ['gpt-4', 'gpt-3.5-turbo']:
        model = OpenAIModel(model_name)
        
    if model == None:
        raise ValueError(f"Invalid model: {model_name}")

    agent_config = next((agent for agent in settings['agents'] if agent['role'] == agent_role), None)

    if agent_config == None:
        raise ValueError(f"Invalid agent: {agent_role}")

    response = conversation.send_message(message, model, agent_config)

    return jsonify({"response": response, "agent": agent_config['name']})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

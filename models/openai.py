import openai
import json

class OpenAIModel:
    def __init__(self, model_name):
        with open('./settings.json') as file:
            openai.api_key = json.load(file)['api_keys']['openai']

        self.model_name = model_name

    def generate_text(self, conversation, temperature):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self._filter_messages(conversation),
            temperature=temperature
        )

        return response['choices'][0]['message']['content'].strip()

    def _filter_messages(self, messages):
        return [{k: v for k, v in msg.items() if k != 'sender'} for msg in messages]

class Conversation:
    def __init__(self):
        self.history = []

    def send_message(self, prompt, model, agent_config):
        agent_name = agent_config['name']

        if not any(item.get('sender') == agent_name for item in self.history):
            self._append_system_message(agent_config['instruction'])

        self._append_user_message(prompt)

        response = model.generate_text(self.history, agent_config['temperature'])

        self._append_agent_message(response, agent_name)

        return response

    def _append_system_message(self, instruction):
        self.history.append({
            'role': 'system',
            'content': instruction
        })

    def _append_user_message(self, message):
        self.history.append({
            'role': 'user',
            'content': message,
            'sender': 'You'
        })

    def _append_agent_message(self, message, name):
        self.history.append({
            'role': 'assistant',
            'content': message,
            'sender': name
        })

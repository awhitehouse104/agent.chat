import json
import click
from rich.console import Console
from rich.markdown import Markdown
from models.openai import OpenAIModel
from conversation import Conversation

console = Console()

with open('./settings.json') as file:
    settings = json.load(file)

def start_conversation(model, agent_config, conversation):
    prompt = ''
    multiline = False
    multiline_first = False

    while True:
        user_input = console.input('[bold yellow][You][/bold yellow]\n' if not multiline or multiline_first else '')
        
        if user_input.lower() in ['/h', '/help']:
            console.print(f"[bright_black]# /l or /multi - toggle multiline ({'on' if multiline else 'off'})[/bright_black]")
            console.print('[bright_black]# /s or /submit - submit prompt (multiline only)[/bright_black]')
            console.print('[bright_black]# /a or /agent - switch agent[/bright_black]')
            console.print('[bright_black]# /m or /model - switch model[/bright_black]')
            console.print('[bright_black]# /c or /clear - clear conversation[/bright_black]')
            console.print('[bright_black]# /q or /quit - quit[/bright_black]')
            continue

        if user_input.lower() in ['/l', '/multi']:
            multiline = not multiline
            multiline_status = 'On' if multiline else 'Off'
            multiline_first = multiline
            if multiline:
                console.print(f"[bold green]Multiline {multiline_status}[/bold green]")
            else:
                console.print(f"[bold red]Multiline {multiline_status}[/bold red]")
            continue

        if user_input.lower() in ['/a', '/agent']:
            agent_options = [agent['role'] for agent in settings['agents']]
            agent_config = get_agent_config(select(agent_options))
            continue

        if user_input.lower() in ['/m', '/model']:
            model_options = settings['models']
            model = OpenAIModel(select(model_options))
            continue

        if user_input.lower() in ['/c', '/clear']:
            conversation.history.clear()
            console.clear()
            continue

        if user_input.lower() in ['/q', '/quit']:
            break

        if multiline:
            if user_input.lower() in ['/s', '/submit']:
                prompt = prompt.replace('/s', '').replace('/submit', '')
                multiline_first = True
            else:
                prompt += user_input
                multiline_first = False
                continue

        prompt += user_input
        response = conversation.send_message(prompt, model, agent_config)
        prompt = ''
        console.print(f"\n[bold blue][{agent_config['name']}][/bold blue] [bright_black]({agent_config['role']} | {model.model_name})[/bright_black]")
        console.print(Markdown(response))
        console.print()

def select(options):
    for i, option in enumerate(options, 1):
        console.print(f"{i}. {option}")
    selection = int(console.input())
    console.print(f"[bold green]Switched to {options[selection -1]}[/bold green]")
    return options[selection - 1]

def get_agent_config(role):
    return next((agent for agent in settings['agents'] if agent['role'] == role), None)

@click.command()
def main():
    console.clear()

    agent_options = [agent['role'] for agent in settings['agents']]
    model_options = settings['models']

    console.print('[bold green]Select Agent[/bold green]')
    agent_role = select(agent_options)
    console.clear()
    
    console.print('[bold green]Select Model[/bold green]')
    model_name = select(model_options)
    console.clear()

    model = OpenAIModel(model_name)
    agent_config = get_agent_config(agent_role)
    conversation = Conversation()

    console.print('[bright_black]# Multiline off[/bright_black]')
    console.print('[bright_black]# Enter /h or /help for a list of commands[/bright_black]\n')

    start_conversation(model, agent_config, conversation)

if __name__ == "__main__":
    main()

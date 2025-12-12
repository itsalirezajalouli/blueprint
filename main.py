import os
import textwrap as tw
from utils import Colors, Agent
from dotenv import load_dotenv
from schemas import get_temp_tool_schema
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.environ.get('HF_TOKEN')

def main():
    client = InferenceClient(
        model = 'moonshotai/Kimi-K2-Thinking',
        token = HF_TOKEN,
    )
    pretty_print('Client is set.')
    system_prompt = 'You are a helpful assistant that is capable of retrieving ' \
        'information about the temperature of a given city.'

    tools = [get_temp_tool_schema]

    agent = Agent(client = client, system_prompt = system_prompt, tools = tools)

    agent('What is the temperature in paris? whats the celsius equivalent of it?')

def pretty_print(input: str, mode: str = 'inf'):
    c = Colors()
    if mode.lower() == 'inf':
        print(f'{c.bold}{c.green}➜ INFO: {c.reset}{input}')
    elif mode.lower() == 'err':
        print(f'{c.bold}{c.red}➜ ERROR: {c.reset}{input}')

if __name__ == "__main__":
    main()

import json
from tools import *
from huggingface_hub import InferenceClient

class Colors:
    green = '\033[92m'
    red = '\033[91m'
    cyan = '\033[96m'
    reset = '\033[0m'
    bold = '\033[1m'

class Agent:
    def __init__(self,
                 client: InferenceClient,
                 system_prompt: str,
                 tools: list[dict],
                 ) -> None:
        self.client = client
        self.system_prompt = system_prompt
        self.messages: list = []
        self.tools = tools if tools is not None else []
        if self.system_prompt:
            self.messages.append(
                {'role': 'system', 'content': system_prompt}
            )

    def __call__(self, msg: str = '') -> None:
        self.messages.append(
            {'role': 'user', 'content': msg}
        )
        final_assisstant_content = self.execute()
        if final_assisstant_content:
            self.messages.append(
                {'role': 'assisstant',
                 'content': final_assisstant_content}
            )
        return final_assisstant_content

    def execute(self) -> None:
        while True:
            response = self.client.chat.completions.create(
                messages = self.messages,
                tools = self.tools,
                tool_choice = 'auto',
            )

            msg = response.choices[0].message

            content = self.tool_call(msg)
            print(content)
            if content is not None: return content

    def tool_call(self, msg):
        if msg.tool_calls:
            self.messages.append(msg)
            tool_outputs = []
            for tool_call in msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                # globals() returns all the available funcs
                if fn_name in globals() and callable(globals()[fn_name]):
                    fn_to_call = globals()[fn_name]
                    executed_output = fn_to_call(**fn_args)
                    tool_output_content = str(executed_output)
                    print(f'Executing tool: {fn_name} with args {fn_args}, ' +
                        f'Output: {tool_output_content[:500]}...')

                    tool_outputs.append(
                        {
                            'tool_call_id': tool_call.id,
                            'role': 'tool',
                            'name': fn_name,
                            'content': tool_output_content,
                        }
                    )
            self.messages.extend(tool_outputs)
        else: return msg.content


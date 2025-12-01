from openai import OpenAI
import tiktoken
from rich import print
from dotenv import load_dotenv
import os
import json

# Documentation: https://platform.openai.com/docs/overview

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-5-nano"

def num_tokens_from_messages(messages, model="gpt-5-nano"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")


    if model == "gpt-5-nano":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    

class OpenAIManager:

    def __init__(self, key = OPEN_API_KEY, history_backup_file = None):
        self.history = []
        self.client = OpenAI(api_key = key)
        self.history_backup_file = history_backup_file

        if self.history_backup_file and os.path.exists(self.history_backup_file):
            with open(self.history_backup_file, 'r') as file:
                self.history = json.load(file)
    
    def update_history(self, prompt):
        # message marked as user because prompt is from elsewhere
        self.history.append({"role": "user", "content": prompt})
        self.save_backup()
    
    def save_backup(self):
        if self.history_backup_file:
            with open(self.history_backup_file, 'w') as file:
                json.dump(self.history, file)

    def create_character(self, character_description):
        if not isinstance(character_description, str):
            print("[red]Please pass in string of text, mission aborted")
        # make sure character doesn't already exist
        elif not self.history: 
            bio = {"role": 'system', 'content': character_description}
            self.history.insert(0, bio)
            self.check_token_limit()

    def chat(self, prompt = ""):
        message = {"role": "user", "content": prompt}

        if prompt == "":
            print("[red]No prompt given :(")
            return 
        
        tokens = num_tokens_from_messages([message])
        print("[yellow]Number of Tokens in Message:", tokens)
        if not tokens < 4096:
            print("[red]message way too long, please save your breath next time")
            return
        
        self._send_message([message], False)
        
    def chat_with_history(self, prompt = ""):
        message = {"role": "user", "content": prompt}

        if prompt == "":
            print("[red]No prompt given :(")
            return 
        
        tokens = num_tokens_from_messages([message])
        # print("[yellow]Number of Tokens in Message:", tokens)
        if tokens < 4096:
            self.history.append(message)
        else:
            print("[red]message way too long, please save your breath next time")
            return

        self.check_token_limit()
        return self._send_message(self.history)

    
    def _send_message(self, messages_to_send, history = True):
        if not isinstance(messages_to_send, list):
            print("[red]Messages should be list, send_message aborted")
            return 
        
        completion = self.client.chat.completions.create(
            model = OPENAI_MODEL,
            messages = messages_to_send,
        )

        message_response = {'role': completion.choices[0].message.role, 'content': completion.choices[0].message.content}

        if history:
            self.history.append(message_response)
            self.save_backup()

        response = completion.choices[0].message.content

        print("[yellow]OpenAI response:")
        print(f"[green]{response}")
        # print("[yellow]Number of Tokens in Response:", num_tokens_from_messages([message_response]))

        return response


    def check_token_limit(self, limit = 4096, range = 100):
        token_count = num_tokens_from_messages(self.history)
        # print("[yellow]History of Conversation is:", token_count, "tokens")
        while token_count > limit - range:
            self.history.pop(1)
            print("[yellow]Adjusted history of convo, new token count:", num_tokens_from_messages(self.history))


if __name__ == '__main__':
    bot = OpenAIManager()
    prompt = "Can you talk about how amazing Real Madrid is. Keep it Brief"
    bot.chat(prompt)

from managers.openai_manager import OpenAIManager
import managers.elevenlabs_manager as ele
from managers.audio_manager import AudioManager

import threading
import time
import random
from rich import print
from queue import Queue

from character_bios import BOT_BIO_1, BOT_BIO_2


audio_queue = Queue()

speaking_lock = threading.Lock()
history_lock = threading.Lock()

radio = AudioManager()
shutdown_event = threading.Event()

bots_paused = False
all_bots: list["Bot"] = []
all_threads = []
human_name = "Achievers"

characters = [
    {"name": "Patrick", "bio": BOT_BIO_1, "voice_id": "Wh0OKIZAclG40RrrGNdD"},
    {"name": "Spongebob", "bio": BOT_BIO_2, "voice_id": "nLrhpssL9P6ZY1ELkUal"},
]

class Bot:
    def __init__(self, name, bio, voice, all_bots: list["Bot"] = None):
        self.name = name
        self.llm = OpenAIManager()
        self.llm.create_character(bio)

        self.voice_id = voice
        self.activated = False
        self.all_bots = all_bots
        self.audio_file_count = 0

    def run(self):
        while not shutdown_event.is_set():
            if bots_paused or not self.activated:
                time.sleep(0.1)
                continue

            self.activated = False

            with history_lock:
                # Generate a response to the conversation
                answer = self.llm.chat_with_history("Okay what is your response. Try to be as chaotic and bizarre as possible. Again, 2 sentences maximum")
                print(f'[magenta]Got the following response:\n{answer}')

                # Add new response into everyone agents chat history
                for bot in self.all_bots:
                    if bot is not self:
                        bot.llm.update_history(f"[{self.name}] {answer}")
            
            audio_file, file_path = ele.text_to_speech_file(answer, self.voice_id, f"{self.name}_audio{self.audio_file_count}")
            self.audio_file_count += 1

            # Wait here until the current speaker is finished
            with speaking_lock:

                # If paused, finish speaking without activating another agent
                if not bots_paused:
                    other_bots = [bot for bot in self.all_bots if bot is not self]
                    random_bot = random.choice(other_bots)
                    random_bot.activated = True
            
                # # Play the audio (without pausing)
                # radio.play_audio(audio_file)
                audio_queue.put({"bot_name": self.name, "audio_file": audio_file, "text": answer})
                time.sleep(radio.get_audio_length(file_path)+1) # so audio doesn't overlap

            print(f"[italic purple] {self.name} has FINISHED")


def init_bots():
    global all_bots, characters
    for char in characters:
        agent = Bot(char["name"], char["bio"], char["voice_id"], all_bots)
        agent_thread = threading.Thread(target=start_bot, args=(agent,))
        agent_thread.start()

        all_bots.append(agent)
        all_threads.append(agent_thread)


def handle_stt(text):
    global bots_paused, all_bots

    bots_paused = True
    print(f"[italic green]{human_name} started speaking")

    with speaking_lock:
        for bot in all_bots:
            bot.llm.update_history(f"[{human_name}] {text}")

    print(f"[italic magenta]{human_name} finished speaking")

    # Activate random bot
    bots_paused = False
    other_bots = [b for b in all_bots]
    random_bot = random.choice(other_bots)
    random_bot.activated = True
    print(f"[cyan]Activating bot {random_bot.name}")

def pause_bots():
    global bots_paused
    print("[italic red] Agents have been paused")
    bots_paused = True

def start_bot(bot):
    bot.run()

def shutdown():
    global all_threads
    shutdown_event.set()
    for t in all_threads:
        t.join()

def get_audio():
    if audio_queue.empty():
        return {"status": "empty"}
    item = audio_queue.get()

    return {
        "status": "contains",
        "bot_name": item["bot_name"],
        "text": item["text"],
        "audio_url": f"/static/{item['audio_file']}"
    }


if __name__ == "__main__":
    init_bots()
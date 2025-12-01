## Multi-Character Chatbots

This code runs a web app were you can converse with multiple chatgpt based characters. Using Microsoft Azure for Speech-to-text, ElevenLabs for custom text-to-speech, and OpenAI for text generation, you are able to talk with multiple GPT Agents. Additionally, the GPT Agents are able to talk with each other, mimicking an actual group conversation/debate.

Currently, the code is set up to run 2 GPT agents, but should be able to handle 3+ with changes to the UI being necessary

# Setting up the project

To use the project you will need:
1. An API Key from [OpenAI]
2. An API Key from [ElevenLabs]
3. An API Key from [Microsoft Azure]

Linked is a guide to setting up each service

Create a .env file within the server and declare your API Keys
```ini
AZURE_SPEECH_KEY = "Your Azure API Key"
AZURE_SPEECH_REGION = "Your Azure Speech Region"
OPENAI_API_KEY = "Your OpenAI API Key"
ELEVENLABS_API_KEY = "Your ElevenLabs API Key"
```

server/bots.py has the code for running multiple characters using multithreading and server/character_bios.py has the character bios used. I have included custom voice ids for the characters from ElevenLabs, which will need to be replaced with the voice ids you choose to use
```python
characters = [
    {"name": "Patrick", "bio": BOT_BIO_1, "voice_id": "CHANGE_VOICE_ID"},
    {"name": "Spongebob", "bio": BOT_BIO_2, "voice_id": "CHANGE_VOICE_ID"},
]
```

# Running the project
In the server folder run:
```sh
uvicorn main:app
```

In the client folder run
```sh
npm run dev
```

# Related Project
Inspiration for this project comes from DougDoug and his own work with [Multi-Agent GPT Characters]. Credit also goes to the Azure team for creating sample code for integrating their STT service with React ([AzureSpeechReactSample])

[//]:

    [OpenAI]: <https://platform.openai.com/docs/overview>
    [ElevenLabs]: <https://elevenlabs.io/docs/overview>
    [Microsoft Azure]: <https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=new-foundry%2Cmacos&pivots=programming-language-python>
    [Multi-Agent GPT Characters]: <https://github.com/DougDougGithub/Multi-Agent-GPT-Characters>
    [AzureSpeechReactSample]: <https://github.com/Azure-Samples/AzureSpeechReactSample>



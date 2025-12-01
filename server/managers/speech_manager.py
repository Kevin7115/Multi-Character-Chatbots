from dotenv import load_dotenv
import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel

# Documentation: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=macos%2Cterminal&pivots=programming-language-python

class stt_input(BaseModel):
    text: str


load_dotenv()

SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

router = APIRouter(
    prefix="/speech"
)

@router.get("/get_token_object")
def get_token_object():
    url = f"https://{SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        "Ocp-Apim-Subscription-Key": SPEECH_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp = requests.post(url, headers=headers)
    token = resp.text
    return {"token": token, "region": SPEECH_REGION}

@router.post("/receive_text")
def recieve(stt: stt_input):
    return {"text": stt.text, "worked": "yes"}
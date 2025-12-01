from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from managers.speech_manager import router as stt_auth_router
from pydantic import BaseModel
from contextlib import asynccontextmanager
from bots import handle_stt, init_bots, shutdown, pause_bots, get_audio

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_bots()
    yield
    shutdown()

class stt_input(BaseModel):
    text: str

app = FastAPI(lifespan=lifespan)
app.include_router(stt_auth_router)

app.mount("/static", StaticFiles(directory="audio"), name="static")

@app.post("/send_stt")
def receive_text(stt: stt_input):
    handle_stt(stt.text)
    return {"status": "ok"}

@app.post("/pause")
def pause_discussion():
    pause_bots()
    return {"status": "ok"}

@app.get("/get_next_audio")
def get_next_audio():
    audio = get_audio()
    return audio
    
@app.get('/')
def main():
    return "Multi-Chatbot API"


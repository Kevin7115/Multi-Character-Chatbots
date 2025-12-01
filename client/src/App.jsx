import { useState, useEffect} from 'react'
import './App.css'
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk";
import { ResultReason } from 'microsoft-cognitiveservices-speech-sdk';
import { getTokenOrRefresh } from './token_util';
import patrick_img from './assets/patrick_img.jpeg'
import spongebob_img from './assets/spongebob_img.webp'

function App() {
  const [displayText, setDisplayText] = useState('INITIALIZED: ready to speech...');
  const [polling, _] = useState(true);
  const [activeSpeaker, setActiveSpeaker] = useState(null);

  async function sttFromMic() {
    const tokenObj = await getTokenOrRefresh();

    const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(tokenObj.authToken, tokenObj.region);
    speechConfig.speechRecognitionLanguage = 'en-US';

    const audioConfig = speechsdk.AudioConfig.fromDefaultMicrophoneInput();
    const recognizer = new speechsdk.SpeechRecognizer(speechConfig, audioConfig);

    const result = await new Promise((resolve, reject) => {
      recognizer.recognizeOnceAsync(
        (res) => resolve(res),
        (err) => reject(err)
      );
    });

    // Now result is available here
    if (result.reason === ResultReason.RecognizedSpeech) {
      setDisplayText(`RECOGNIZED: Text=${result.text}`);
    } else {
      setDisplayText("ERROR: Could not recognize speech.");
      return;
    }


    const res = await fetch("/api/send_stt", {
      method: "POST",
      body: JSON.stringify({
        text: result.text,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });
    const data = await res.json();
    console.log(`Data: ${data.text} and ${data.worked}`);
  }

  async function pollBotAudio() {
    if (!polling) return;

    const res = await fetch("/api/get_next_audio");
    const data = await res.json();

    if (data.status !== "empty") {
      // Update display text
      console.log(`${data.bot_name}: ${data.text}`)
      setDisplayText(`${data.bot_name}: ${data.text}`);

      // Play audio
      console.log(data.audio_url);
      setActiveSpeaker(data.bot_name);
      const audio = new Audio(`/api${data.audio_url}`);

      audio.onended = () => {
        setActiveSpeaker(null);
      };
      
      audio.play();
    }

    // Poll again in 0.5s
    setTimeout(pollBotAudio, 500);
  }

  // start polling when component mounts
  useEffect(() => {
    pollBotAudio();
  }, []);

  async function pauseBots() {
    const res = await fetch("/api/pause", {
      method: "POST",
      // body: JSON.stringify({
      //   text: result.text,
      // }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });
    const data = await res.json();
    console.log(`Status: ${data.status}`);
  }

  return (
    <>
      <div className="app-container">

        <div className="images-row">
          <div className={`character ${activeSpeaker === "Spongebob" ? "speaking" : ""}`}>
            <img src={spongebob_img} width={300} height={300}/>
          </div>

          <div className={`character ${activeSpeaker === "Patrick" ? "speaking" : ""}`}>
            <img src={patrick_img} width={300} height={300}/>
          </div>
        </div>

        <div className="controls-row">
          <button className="icon-btn" onClick={() => sttFromMic()}>
            🎤
          </button>

          <button className="icon-btn" onClick={() => pauseBots()}>
            ⏸️
          </button>
        </div>

        <div className="output-box">
          <code>{displayText}</code>
        </div>

      </div>
    </>
  )
}

export default App

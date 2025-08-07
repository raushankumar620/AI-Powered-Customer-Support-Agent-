# call_response.py
import openai
from voice.audio_utils import download_audio, convert_mp3_to_wav, clean_temp_audio
from agent.query_agent import query_agent
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Env var से key लो

def transcribe_audio(audio_url):
    mp3_path = download_audio(audio_url)
    wav_path = convert_mp3_to_wav(mp3_path)
    
    with open(wav_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    
    clean_temp_audio()
    return transcript["text"]

def generate_response(user_message, system_prompt=None):
    # Use the vector-based query agent for better responses
    if user_message:
        return query_agent(user_message)
    else:
        return "I'm sorry, I didn't understand that. Could you please repeat your question?"

def handle_call(audio_url):
    print("🔊 Transcribing call...")
    user_text = transcribe_audio(audio_url)
    print("🧠 User said:", user_text)

    system_knowledge = "You are a helpful assistant for Nextcore AI. You know about the company's services and technologies."
    reply_text = generate_response(user_text, system_prompt=system_knowledge)
    
    print("🤖 Agent reply:", reply_text)
    return reply_text

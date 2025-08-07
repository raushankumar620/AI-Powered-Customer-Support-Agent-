# speech_to_text.py
import openai
import os
from agent.config import OPENAI_API_KEY
from voice.audio_utils import download_audio, convert_mp3_to_wav, clean_temp_audio
import logging

logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def transcribe_audio_file(audio_file_path):
    """
    Transcribe audio file using OpenAI Whisper API
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return None

def speech_to_text(audio_path):
    """Legacy function for backward compatibility"""
    return transcribe_audio_file(audio_path)

def transcribe_from_url(audio_url):
    """
    Download audio from URL and transcribe it
    """
    try:
        # Download audio
        mp3_path = download_audio(audio_url)
        
        # Convert to WAV if needed
        wav_path = convert_mp3_to_wav(mp3_path)
        
        # Transcribe
        transcript = transcribe_audio_file(wav_path)
        
        # Clean up temporary files
        clean_temp_audio()
        
        return transcript
    except Exception as e:
        logger.error(f"Error processing audio from URL: {str(e)}")
        return None

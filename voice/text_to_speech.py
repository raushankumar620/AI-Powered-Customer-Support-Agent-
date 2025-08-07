# text_to_speech.py
import requests
import os
import boto3
from agent.config import *
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

def text_to_speech_elevenlabs(text, output_path="data/recordings/output.mp3"):
    """Convert text to speech using ElevenLabs API"""
    try:
        API_KEY = os.getenv("ELEVENLABS_API_KEY")
        voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        body = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }

        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        else:
            logger.error(f"ElevenLabs API error: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error with ElevenLabs TTS: {str(e)}")
        return None

def text_to_speech_polly(text, voice_id='Joanna', output_format='mp3'):
    """Convert text to speech using Amazon Polly"""
    try:
        polly_client = boto3.client(
            'polly',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
        
        return response['AudioStream'].read()
        
    except Exception as e:
        logger.error(f"Error with Polly TTS: {str(e)}")
        return None

def text_to_speech_openai(text, voice='alloy', output_path=None):
    """Convert text to speech using OpenAI TTS API"""
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        if output_path:
            response.stream_to_file(output_path)
            return output_path
        else:
            return response.content
            
    except Exception as e:
        logger.error(f"Error with OpenAI TTS: {str(e)}")
        return None

# Default function for backward compatibility
def text_to_speech(text, output_path="data/recordings/output.mp3"):
    """Default TTS function - tries ElevenLabs first, falls back to OpenAI"""
    result = text_to_speech_elevenlabs(text, output_path)
    if result is None:
        logger.info("ElevenLabs failed, trying OpenAI TTS...")
        return text_to_speech_openai(text, output_path=output_path)
    return result
